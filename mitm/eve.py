import os
import sys

import argparse

from common import *
from const import *


parser = argparse.ArgumentParser()
parser.add_argument("--relay", help="Relay message from Bob to Alice.", action="store_true")
parser.add_argument("--break-heart", help="Alice is going to break Bob's heart.", action="store_true")
parser.add_argument("--custom", help="Send custom message.", action="store_true")
args = parser.parse_args()

if args.relay:
    print("EVE IS ON RELAY MODE")
elif args.break_heart:
    print("EVE IS ON BREAK HEART MODE")
elif args.custom:
    print("EVE IS ON CUSTOM MODE")

print('=========================================')

dialog = Dialog('print')

# establishing a socket pretending im alice
print('PRETENDING TO BE ALICE...')
player1 = 'alice'
alice_socket, alice_aes = setup(player1, BUFFER_DIR, BUFFER_FILE_NAME)
os.rename(BUFFER_DIR + BUFFER_FILE_NAME, BUFFER_DIR + "new_buffer")
print('SOCKETS FOR COMMUNICATION WITH BOB ESTABLISHED!')

# sockets for communication with alice (I AM BOB)
print('PRETENDING TO BE BOB...')
player2 = 'bob'
bob_socket, bob_aes = setup(player2, BUFFER_DIR, BUFFER_FILE_NAME)
print('SOCKETS FOR COMMUNICATION WITH ALICE ESTABLISHED!')

received_from_alice = receive_and_decrypt(bob_aes, bob_socket) # message from alice

# ======================================= RELAY MODE =======================================
if args.relay:
    if CUSTOM_CHAT:
        dialog.prompt('Please input message...')
        to_send = input()
    else:
        to_send = NICE_MSG[player1]

    encrypt_and_send(to_send, alice_aes, alice_socket)
    dialog.chat('Alice said: "{}"'.format(to_send))

    dialog.info('Message sent! Waiting for reply...')
    received_from_bob = receive_and_decrypt(alice_aes, alice_socket)

    dialog.chat('Bob said: "{}"'.format(received_from_bob))

    encrypt_and_send(received_from_bob, bob_aes, bob_socket)

    tear_down(alice_socket, BUFFER_DIR, "new_buffer")
    tear_down(bob_socket, BUFFER_DIR, BUFFER_FILE_NAME)

# ======================================= BREAK-HEART MODE =======================================
elif args.break_heart:
    to_send = BAD_MSG[player1] # CHANGE NICE_MSG TO BAD_MSG

    # alice encrypts message and sends to bob
    encrypt_and_send(to_send, alice_aes, alice_socket)
    dialog.chat('Alice said: "{}"'.format(to_send))

    dialog.info('Message sent! Waiting for reply...')
    received_from_bob = receive_and_decrypt(alice_aes, alice_socket)

    dialog.chat('Bob said: "{}"'.format(received_from_bob))

    encrypt_and_send(received_from_bob, bob_aes, bob_socket)

    tear_down(alice_socket, BUFFER_DIR, "new_buffer")
    tear_down(bob_socket, BUFFER_DIR, BUFFER_FILE_NAME)

# ======================================= CUSTOM MODE =======================================
elif args.custom:
    dialog.prompt('Input what you would like Alice to say to Bob')
    alice_send = input()

    # alice encrypts message and sends to bob
    encrypt_and_send(alice_send, alice_aes, alice_socket)
    dialog.chat('Alice said: "{}"'.format(alice_send))

    dialog.info('Message sent! Waiting for reply...')
    received_from_bob = receive_and_decrypt(alice_aes, alice_socket)

    dialog.prompt('Input what you would like Bob to say to Alice')
    bob_send = input()

    dialog.chat('Bob said: "{}"'.format(received_from_bob))

    encrypt_and_send(bob_send, bob_aes, bob_socket)

    tear_down(alice_socket, BUFFER_DIR, "new_buffer")
    tear_down(bob_socket, BUFFER_DIR, BUFFER_FILE_NAME)

