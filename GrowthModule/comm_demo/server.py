#!/usr/bin/env python

import socket

ENCODING = 'utf-8'

TCP_IP = '127.0.0.1'
TCP_PORT = 8503
BUFFER_SIZE = 4096

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)  # the argument (1) specifies the number of unaccepted connections that the system will allow before
# refusing new connections.

conn, addr = s.accept()
print('Connection address:', addr)
msgs_buff = ""
while True:
    data = conn.recv(BUFFER_SIZE)
    if not data: break
    msgs_buff += data.decode(ENCODING)
    msgs = msgs_buff.split(";;")
    if len(msgs) > 1:  # there is an untreated message
        print(f"Received msg: {msgs[0]}\n")
        if msgs[0] == "atr_read;temperature":
            # send response
            conn.send("atr_res;temperature;23.5;;".encode(ENCODING))

        # update msgs_buff because first message treated
        msgs_buff = ';;'.join(msgs[1:])

print("Communication ended")
conn.close()
