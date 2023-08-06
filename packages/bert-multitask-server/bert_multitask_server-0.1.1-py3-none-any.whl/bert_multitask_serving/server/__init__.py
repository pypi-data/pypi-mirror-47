#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Han Xiao <artex.xh@gmail.com> <https://hanxiao.github.io>
import multiprocessing
import os
import random
import sys
import threading
import time
from collections import defaultdict
from datetime import datetime
from multiprocessing import Process
import tensorflow as tf
import pickle

import numpy as np
import zmq
import zmq.decorators as zmqd
from termcolor import colored
from zmq.utils import jsonapi
import re

from bert_multitask_learning import FullTokenizer
from bert_multitask_learning import get_or_make_label_encoder
from bert_multitask_learning import BaseParams
from bert_multitask_learning import to_serving_input

from .helper import *
from .zmq_decor import multi_socket
from .result_parser import parse_prediction

__all__ = ['__version__', 'BertServer']
__version__ = '1.0.0'

_tf_ver_ = check_tf_version()


class ServerCommand:
    terminate = b'TERMINATION'
    show_config = b'SHOW_CONFIG'
    new_job = b'REGISTER'

    @staticmethod
    def is_valid(cmd):
        return any(not k.startswith('__') and v == cmd for k, v in vars(ServerCommand).items())


class BertServer(threading.Thread):
    def __init__(self, args):
        super().__init__()
        self.logger = set_logger(
            colored('VENTILATOR', 'magenta'), args.verbose)

        self.model_dir = args.model_dir
        # self.max_seq_len = args.max_seq_len
        self.num_worker = args.num_worker
        self.max_batch_size = args.max_batch_size
        # optimize concurrency for multi-clients
        self.num_concurrent_socket = max(8, args.num_worker * 2)
        self.port = args.port
        self.args = args
        self.status_args = {k: (v if k != 'pooling_strategy' else v.value)
                            for k, v in sorted(vars(args).items())}
        self.status_static = {
            'tensorflow_version': _tf_ver_,
            'python_version': sys.version,
            'server_version': __version__,
            'pyzmq_version': zmq.pyzmq_version(),
            'zmq_version': zmq.zmq_version(),
            'server_start_time': str(datetime.now()),
        }
        self.processes = []
        self.logger.info(
            'freeze, optimize and export graph, could take a while...')

        params = BaseParams()
        params.from_json(os.path.join(self.model_dir, 'params.json'))
        base_dir, dir_name = os.path.split(self.model_dir)
        params.assign_problem(
            self.args.problem, base_dir=base_dir, dir_name=dir_name, is_serve=True)

        self.max_seq_len = params.max_seq_len
        setattr(self.args, 'params', params)

        self.graph_path = os.path.join(self.model_dir, 'export_model')
        # from .graph import optimize_graph
        # self.graph_path = optimize_graph(self.args, self.logger)
        if self.graph_path:
            self.logger.info('optimized graph is stored at: %s' %
                             self.graph_path)
        else:
            self.graph_path = tf.train.latest_checkpoint(
                self.model_dir) + '.meta'
            # raise FileNotFoundError(
            #     'graph optimization fails and returns empty result')

    def close(self):
        self.logger.info('shutting down...')
        self._send_close_signal()
        for p in self.processes:
            p.close()
        self.join()

    @zmqd.context()
    @zmqd.socket(zmq.PUSH)
    def _send_close_signal(self, _, frontend):
        frontend.connect('tcp://localhost:%d' % self.port)
        frontend.send_multipart([b'', ServerCommand.terminate, b'', b''])

    def run(self):
        self._run()

    @zmqd.context()
    @zmqd.socket(zmq.PULL)
    @zmqd.socket(zmq.PAIR)
    @multi_socket(zmq.PUSH, num_socket='num_concurrent_socket')
    def _run(self, _, frontend, sink, *backend_socks):

        def push_new_job(_job_id, _json_msg, _msg_len):
            # backend_socks[0] is always at the highest priority
            _sock = backend_socks[0] if _msg_len <= self.args.priority_batch_size else rand_backend_socket
            _sock.send_multipart([_job_id, _json_msg])

        # bind all sockets
        self.logger.info('bind all sockets')
        frontend.bind('tcp://*:%d' % self.port)
        addr_front2sink = auto_bind(sink)
        addr_backend_list = [auto_bind(b) for b in backend_socks]
        self.logger.info('open %d ventilator-worker sockets' %
                         len(addr_backend_list))

        # start the sink process
        self.logger.info('start the sink')
        proc_sink = BertSink(self.args, addr_front2sink)
        self.processes.append(proc_sink)
        proc_sink.start()
        addr_sink = sink.recv().decode('ascii')

        # start the backend processes
        device_map = self._get_device_map()
        for idx, device_id in enumerate(device_map):
            process = BertWorker(idx, self.args, addr_backend_list, addr_sink, device_id,
                                 self.graph_path)
            self.processes.append(process)
            process.start()

        rand_backend_socket = None
        server_status = ServerStatistic()
        while True:
            try:
                request = frontend.recv_multipart()
            except ValueError:
                self.logger.error(
                    'received a wrongly-formatted request (expected 4 frames, got %d)' % len(request))
                self.logger.error('\n'.join('field %d: %s' % (idx, k)
                                            for idx, k in enumerate(request)), exc_info=True)
            else:
                client, msg, req_id, msg_len = request
                server_status.update(request)
                if msg == ServerCommand.terminate:
                    break
                elif msg == ServerCommand.show_config:
                    self.logger.info(
                        'new config request\treq id: %d\tclient: %s' % (int(req_id), client))
                    status_runtime = {'client': client.decode('ascii'),
                                      'num_process': len(self.processes),
                                      'ventilator -> worker': addr_backend_list,
                                      'worker -> sink': addr_sink,
                                      'ventilator <-> sink': addr_front2sink,
                                      'server_current_time': str(datetime.now()),
                                      'statistic': server_status.value,
                                      'device_map': device_map,
                                      'num_concurrent_socket': self.num_concurrent_socket}

                    sink.send_multipart([client, msg, jsonapi.dumps({**status_runtime,
                                                                     **self.status_args,
                                                                     **self.status_static}), req_id])
                else:
                    self.logger.info('new encode request\treq id: %d\tsize: %d\tclient: %s' %
                                     (int(req_id), int(msg_len), client))
                    # register a new job at sink
                    sink.send_multipart(
                        [client, ServerCommand.new_job, msg_len, req_id])

                    # renew the backend socket to prevent large job queueing up
                    # [0] is reserved for high priority job
                    # last used backennd shouldn't be selected either as it may be queued up already
                    rand_backend_socket = random.choice(
                        [b for b in backend_socks[1:] if b != rand_backend_socket])

                    # push a new job, note super large job will be pushed to one socket only,
                    # leaving other sockets free
                    job_id = client + b'#' + req_id
                    if int(msg_len) > self.max_batch_size:
                        seqs = jsonapi.loads(msg)
                        job_gen = ((job_id + b'@%d' % i, seqs[i:(i + self.max_batch_size)]) for i in
                                   range(0, int(msg_len), self.max_batch_size))
                        for partial_job_id, job in job_gen:
                            push_new_job(partial_job_id,
                                         jsonapi.dumps(job), len(job))
                    else:
                        push_new_job(job_id, msg, int(msg_len))

        self.logger.info('terminated!')

    def _get_device_map(self):
        self.logger.info('get devices')
        run_on_gpu = False
        device_map = [-1] * self.num_worker
        if not self.args.cpu:
            try:
                import GPUtil
                num_all_gpu = len(GPUtil.getGPUs())
                avail_gpu = GPUtil.getAvailable(
                    order='memory', limit=min(num_all_gpu, self.num_worker))
                num_avail_gpu = len(avail_gpu)

                if num_avail_gpu >= self.num_worker:
                    run_on_gpu = True
                elif 0 < num_avail_gpu < self.num_worker:
                    self.logger.warning('only %d out of %d GPU(s) is available/free, but "-num_worker=%d"' %
                                        (num_avail_gpu, num_all_gpu, self.num_worker))
                    if not self.args.device_map:
                        self.logger.warning('multiple workers will be allocated to one GPU, '
                                            'may not scale well and may raise out-of-memory')
                    else:
                        self.logger.warning('workers will be allocated based on "-device_map=%s", '
                                            'may not scale well and may raise out-of-memory' % self.args.device_map)
                    run_on_gpu = True
                else:
                    self.logger.warning('no GPU available, fall back to CPU')

                if run_on_gpu:
                    device_map = ((self.args.device_map or avail_gpu)
                                  * self.num_worker)[: self.num_worker]
            except FileNotFoundError:
                self.logger.warning('nvidia-smi is missing, often means no gpu on this machine. '
                                    'fall back to cpu!')
        self.logger.info('device map: \n\t\t%s' % '\n\t\t'.join(
            'worker %2d -> %s' % (w_id, ('gpu %2d' % g_id) if g_id >= 0 else 'cpu') for w_id, g_id in
            enumerate(device_map)))
        return device_map


class BertSink(Process):
    def __init__(self, args, front_sink_addr):
        super().__init__()
        self.port = args.port_out
        self.exit_flag = multiprocessing.Event()
        self.logger = set_logger(colored('SINK', 'green'), args.verbose)
        self.front_sink_addr = front_sink_addr

    def close(self):
        self.logger.info('shutting down...')
        self.exit_flag.set()
        self.terminate()
        self.join()
        self.logger.info('terminated!')

    def run(self):
        self._run()

    @zmqd.socket(zmq.PULL)
    @zmqd.socket(zmq.PAIR)
    @zmqd.socket(zmq.PUB)
    def _run(self, receiver, frontend, sender):
        receiver_addr = auto_bind(receiver)
        frontend.connect(self.front_sink_addr)
        sender.bind('tcp://*:%d' % self.port)

        pending_checksum = defaultdict(int)
        pending_result = defaultdict(list)
        job_checksum = defaultdict(int)

        poller = zmq.Poller()
        poller.register(frontend, zmq.POLLIN)
        poller.register(receiver, zmq.POLLIN)

        # send worker receiver address back to frontend
        frontend.send(receiver_addr.encode('ascii'))

        self.logger.info('ready')

        while not self.exit_flag.is_set():
            socks = dict(poller.poll())
            if socks.get(receiver) == zmq.POLLIN:
                msg = receiver.recv_multipart()
                job_id = msg[0]
                # parsing the ndarray
                arr_info, arr_val = jsonapi.loads(
                    msg[1]), jsonapi.loads(msg[2])
                # X = np.frombuffer(memoryview(arr_val),
                #                   dtype=arr_info['dtype'])
                # X = X.reshape(arr_info['shape'])

                X = {k: np.array(v) for k, v in arr_val.items()}

                job_info = job_id.split(b'@')
                job_id = job_info[0]
                partial_id = job_info[1] if len(job_info) == 2 else 0
                pending_result[job_id].append((X, partial_id))
                pending_checksum[job_id] += X[list(X.keys())[0]].shape[0]
                self.logger.info('collect job %s (%d/%d)' % (job_id,
                                                             pending_checksum[job_id],
                                                             job_checksum[job_id]))

                # check if there are finished jobs, send it back to workers
                finished = [(k, v) for k, v in pending_result.items()
                            if pending_checksum[k] == job_checksum[k]]
                for job_info, tmp in finished:
                    self.logger.info('send back\tsize: %d\tjob id:%s\t' % (
                        job_checksum[job_info], job_info))
                    # re-sort to the original order
                    tmp = [x[0] for x in sorted(
                        tmp, key=lambda x: int(x[1]))]
                    new_tmp_dict = defaultdict(list)
                    for pred_dict in tmp:
                        for problem, pred in pred_dict.items():
                            new_tmp_dict[problem] += pred.tolist()
                    # for problem in new_tmp_dict:
                    #     new_tmp_dict[problem] = np.concatenate(
                    #         new_tmp_dict[problem], axis=0)

                    client_addr, req_id = job_info.split(b'#')
                    send_dict_ndarray(sender, client_addr,
                                      new_tmp_dict, req_id)
                    pending_result.pop(job_info)
                    pending_checksum.pop(job_info)
                    job_checksum.pop(job_info)

            if socks.get(frontend) == zmq.POLLIN:
                client_addr, msg_type, msg_info, req_id = frontend.recv_multipart()
                if msg_type == ServerCommand.new_job:
                    job_info = client_addr + b'#' + req_id
                    job_checksum[job_info] = int(msg_info)
                    self.logger.info('job register\tsize: %d\tjob id: %s' % (
                        int(msg_info), job_info))
                elif msg_type == ServerCommand.show_config:
                    # dirty fix of slow-joiner: sleep so that client receiver can connect.
                    time.sleep(0.1)
                    self.logger.info('send config\tclient %s' % client_addr)
                    sender.send_multipart([client_addr, msg_info, req_id])


class BertWorker(Process):
    def __init__(self, id, args, worker_address_list, sink_address, device_id, graph_path):
        super().__init__()
        self.worker_id = id
        self.device_id = device_id
        self.logger = set_logger(
            colored('WORKER-%d' % self.worker_id, 'yellow'), args.verbose)
        # self.max_seq_len = args.max_seq_len
        self.mask_cls_sep = args.mask_cls_sep
        self.daemon = True
        self.exit_flag = multiprocessing.Event()
        self.worker_address = worker_address_list
        self.num_concurrent_socket = len(self.worker_address)
        self.sink_address = sink_address
        # set to zero for CPU-worker
        self.prefetch_size = args.prefetch_size if self.device_id > 0 else None
        self.gpu_memory_fraction = args.gpu_memory_fraction
        self.model_dir = args.model_dir
        self.verbose = args.verbose
        self.graph_path = graph_path
        self.args = args

        self.params = BaseParams()
        self.params.from_json(os.path.join(self.model_dir, 'params.json'))
        base_dir, dir_name = os.path.split(self.model_dir)
        self.params.assign_problem(
            self.args.problem, base_dir=base_dir, dir_name=dir_name, is_serve=True)

        self.max_seq_len = self.params.max_seq_len
        self.problem_list = sorted(re.split(r'[&|]', self.args.problem))

        self.label_encoder_dict = {
            problem: get_or_make_label_encoder(self.params, problem, 'predict') for problem in self.problem_list}
        self.tokenizer = FullTokenizer(self.params.vocab_file)

    def close(self):
        self.logger.info('shutting down...')
        self.exit_flag.set()
        self.terminate()
        self.join()
        self.logger.info('terminated!')

    def get_estimator(self, tf):
        from tensorflow.python.estimator.estimator import Estimator
        from tensorflow.python.estimator.run_config import RunConfig
        from tensorflow.python.estimator.model_fn import EstimatorSpec

        self.problem_list = sorted(re.split(r'[&|]', self.args.problem))

        def model_fn(features, labels, mode, params):
            with tf.gfile.GFile(self.graph_path, 'rb') as f:
                graph_def = tf.GraphDef()
                graph_def.ParseFromString(f.read())

            input_names = ['input_ids', 'input_mask', 'segment_ids']

            output = tf.import_graph_def(
                graph_def,
                input_map={
                    k + ':0': features[k] for k in input_names},
                return_elements=['%s_top/%s_predict:0' % (
                    self.params.share_top[problem], self.params.share_top[problem])
                    for problem in self.params.problem_list])
            prediction_dict = {
                self.problem_list[ind]: output[ind]
                for ind in range(len(self.problem_list))}
            prediction_dict.update({'client_id': features['client_id'],
                                    'raw_text': features['raw_text']})

            return EstimatorSpec(mode=mode, predictions=prediction_dict)

        config = tf.ConfigProto(
            device_count={'GPU': 0 if self.device_id < 0 else 1},
            intra_op_parallelism_threads=40,
            inter_op_parallelism_threads=40)
        config.gpu_options.allow_growth = True
        config.gpu_options.per_process_gpu_memory_fraction = self.gpu_memory_fraction
        config.log_device_placement = False

        return Estimator(
            model_fn=model_fn,
            model_dir=self.params.ckpt_dir,
            config=RunConfig(session_config=config))

    def run(self):
        self._run()

    @zmqd.socket(zmq.PUSH)
    @multi_socket(zmq.PULL, num_socket='num_concurrent_socket')
    def _run(self, sink, *receivers):
        self.logger.info('use device %s, load graph from %s' %
                         ('cpu' if self.device_id < 0 else ('gpu: %d' % self.device_id), self.graph_path))

        tf = import_tf(self.device_id, self.verbose)
        estimator = self.get_estimator(tf)

        for sock, addr in zip(receivers, self.worker_address):
            sock.connect(addr)

        sink.connect(self.sink_address)
        for r in estimator.predict(self.input_fn_builder(receivers, tf), yield_single_examples=False):
            client_id = r.pop('client_id')
            r = parse_prediction(r, self.label_encoder_dict,
                                 self.tokenizer, self.params)
            r.pop('raw_text')
            send_dict_ndarray(sink, client_id, r)
            # self.logger.info('job done\tsize: %s\tclient: %s' %
            #                  (r['encodes'].shape, r['client_id']))
            self.logger.info('job done\tclient: %s' %
                             (client_id))

    def input_fn_builder(self, socks, tf):
        from .bert.extract_features import convert_lst_to_features
        # from .bert.tokenization import FullTokenizer
        from bert_multitask_learning import FullTokenizer

        def gen():
            tokenizer = FullTokenizer(
                vocab_file=os.path.join(self.model_dir, 'vocab.txt'))
            poller = zmq.Poller()
            for sock in socks:
                poller.register(sock, zmq.POLLIN)

            self.logger.info('ready and listening!')

            while not self.exit_flag.is_set():
                events = dict(poller.poll())
                for sock_idx, sock in enumerate(socks):
                    if sock in events:
                        client_id, raw_msg = sock.recv_multipart()
                        msg = jsonapi.loads(raw_msg)
                        self.logger.info('new job\tsocket: %d\tsize: %d\tclient: %s' % (
                            sock_idx, len(msg), client_id))
                        # tmp_f = list(convert_lst_to_features(msg, self.max_seq_len, tokenizer, self.logger,
                        #                                      is_tokenized, self.mask_cls_sep))
                        self.params.max_seq_len = self.max_seq_len
                        tmp_f = to_serving_input(
                            msg, self.params, mode='predict', tokenizer=tokenizer)
                        yield_dict = {
                            'client_id': client_id,
                            'raw_text': msg,
                            'input_ids': [],
                            'input_mask': [],
                            'segment_ids': []
                        }
                        for d in tmp_f:
                            for k in d:
                                yield_dict[k].append(d[k])
                        yield yield_dict

        def input_fn():
            return (tf.data.Dataset.from_generator(
                gen,
                output_types={'input_ids': tf.int32,
                              'input_mask': tf.int32,
                              'segment_ids': tf.int32,
                              'client_id': tf.string,
                              'raw_text': tf.string},
                output_shapes={
                    'client_id': (),
                    'input_ids': (None, self.max_seq_len),
                    'input_mask': (None, self.max_seq_len),
                    'segment_ids': (None, self.max_seq_len),
                    'raw_text': (None, )}).prefetch(self.prefetch_size))

        return input_fn


class ServerStatistic:
    def __init__(self):
        self._hist_client = defaultdict(int)
        self._hist_msg_len = defaultdict(int)
        self._client_last_active_time = defaultdict(float)
        self._num_data_req = 0
        self._num_sys_req = 0
        self._num_total_seq = 0
        self._last_req_time = time.perf_counter()
        self._last_two_req_interval = []
        self._num_last_two_req = 200

    def update(self, request):
        client, msg, req_id, msg_len = request
        self._hist_client[client] += 1
        self._hist_msg_len[int(msg_len)] += 1
        self._num_total_seq += int(msg_len)
        if ServerCommand.is_valid(msg):
            self._num_sys_req += 1
            # do not count for system request, as they are mainly for heartbeats
        else:
            self._num_data_req += 1
            tmp = time.perf_counter()
            self._client_last_active_time[client] = tmp
            if len(self._last_two_req_interval) < self._num_last_two_req:
                self._last_two_req_interval.append(tmp - self._last_req_time)
            else:
                self._last_two_req_interval.pop(0)
            self._last_req_time = tmp

    @property
    def value(self):
        def get_min_max_avg(name, stat):
            if len(stat) > 0:
                return {
                    'avg_%s' % name: sum(stat) / len(stat),
                    'min_%s' % name: min(stat),
                    'max_%s' % name: max(stat),
                    'num_min_%s' % name: sum(v == min(stat) for v in stat),
                    'num_max_%s' % name: sum(v == max(stat) for v in stat),
                }
            else:
                return {}

        def get_num_active_client(interval=180):
            # we count a client active when its last request is within 3 min.
            now = time.perf_counter()
            return sum(1 for v in self._client_last_active_time.values() if (now - v) < interval)

        parts = [{
            'num_data_request': self._num_data_req,
            'num_total_seq': self._num_total_seq,
            'num_sys_request': self._num_sys_req,
            'num_total_request': self._num_data_req + self._num_sys_req,
            'num_total_client': len(self._hist_client),
            'num_active_client': get_num_active_client()},
            get_min_max_avg('request_per_client', self._hist_client.values()),
            get_min_max_avg('size_per_request', self._hist_msg_len.keys()),
            get_min_max_avg('last_two_interval', self._last_two_req_interval),
            get_min_max_avg('request_per_second', [
                            1. / v for v in self._last_two_req_interval]),
        ]

        return {k: v for d in parts for k, v in d.items()}
