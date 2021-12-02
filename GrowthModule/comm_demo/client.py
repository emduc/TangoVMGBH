#!/usr/bin/env python

import socket

TCP_IP = '127.0.0.1'
TCP_PORT = 8503
BUFFER_SIZE = 7
ENCODING = 'utf-8'
MESSAGE = "atr_read;temperature;;".encode(ENCODING)

NB_MSGS = 3

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
for i in range(NB_MSGS):
    s.send(MESSAGE)
responses_buff = ""
responses = []
while len(responses) < NB_MSGS + 1:
    data = s.recv(BUFFER_SIZE)
    responses_buff += data.decode(ENCODING)
    responses = responses_buff.split(";;")
    print(f"buffer = {responses_buff}")
s.close()

print(f"received data:{responses}")

# One socket per message alternative:

# for i in range(NB_MSGS):
#     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     s.connect((TCP_IP, TCP_PORT))
#     s.send(MESSAGE)
#     responses_buff = ""
#     responses = []
#     while len(responses) <= 1:
#         data = s.recv(BUFFER_SIZE)
#         responses_buff += data.decode(ENCODING)
#         responses = responses_buff.split(";;")
#         print(f"buffer = {responses_buff}")
#     print(f"responses = {responses}")
#     s.close()