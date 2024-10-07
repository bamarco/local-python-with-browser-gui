#!/usr/bin/env python3
import sys

def hello():
    return "Hello, world!"

def pong(ping):
    if ping == 'ping':
        return 'pong'
    else:
        raise Exception(f"Expected 'ping', but received '{ping}'. Pong only responds to 'ping'.")

if __name__ == '__main__':
    try:
        print(pong(sys.argv[1]))
    except IndexError:
        raise Exception(f"Expected 'ping', but received no command line arguments. Pong only responds to 'ping'.")
