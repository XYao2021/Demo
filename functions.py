import pickle
import struct
import argparse
import socket


def args_parser():
    parse = argparse.ArgumentParser()

    parse.add_argument('-server', type=str, default='172.16.0.1', help='Server IP address')
    parse.add_argument('-port', type=int, default=5050, help='Socket port')

    args = parse.parse_args()
    return args

def send_msg(sock, msg):
    msg_pickle = pickle.dumps(msg)
    sock.sendall(struct.pack(">I", len(msg_pickle)))
    sock.send(msg_pickle)

def recv_msg(sock, expect_msg_type=None):
    msg_len = struct.unpack(">I", sock.recv(4))[0]
    msg = sock.recv(msg_len, socket.MSG_WAITALL)
    msg = pickle.loads(msg)

    if (expect_msg_type is not None) and (msg[0] != expect_msg_type):
        raise Exception("Expected " + expect_msg_type + " but received " + msg[0])
    return msg

