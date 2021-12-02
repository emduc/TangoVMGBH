#!/usr/bin/env python

import socket
import time

TCP_IP = '127.0.0.1'
TCP_PORT = 8503
BUFFER_SIZE = 4096
ENCODING = 'utf-8'
MESSAGE = "atr_read;temperature;;".encode(ENCODING)

DELAY_BETWEEN_MSGS = 1.0

MAX_RESPONSE_TIME = 1.0
RESPONSE_POLL_DELAY = 0.1

def try_connecting() -> socket.socket:
    print("Attempting (re)connection...")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connected = False
    while not connected:
        try:
            s.connect((TCP_IP, TCP_PORT))
        except ConnectionRefusedError:
            print(f"Connection to server {TCP_IP}:{TCP_PORT} was refused!")
            time.sleep(1) # so we don't spam the connection attempts
        else:
            connected = True
            print(f"Successful connection to {TCP_IP}:{TCP_PORT}!")
    return s

def main():
    s = try_connecting()
    while True:
        try:
            s.send(MESSAGE)
        except BrokenPipeError:
            print(f"BrokenPipeError on {TCP_IP}:{TCP_PORT}.")
            s.close()
            s = try_connecting()
        responses_buff = ""
        responses = []
        waited_for = 0.0 # wait time, in case of a disconnection of the server
        while len(responses) <= 1 and waited_for <= MAX_RESPONSE_TIME:
            data = s.recv(BUFFER_SIZE)
            responses_buff += data.decode(ENCODING)
            responses = responses_buff.split(";;")
            waited_for += RESPONSE_POLL_DELAY
            time.sleep(RESPONSE_POLL_DELAY)
        if waited_for > MAX_RESPONSE_TIME:
            s.close() # the server has timed out, so we close the socket
            s = try_connecting()
        print(f"responses = {responses}")
        time.sleep(DELAY_BETWEEN_MSGS)

if __name__ == '__main__':
    main()