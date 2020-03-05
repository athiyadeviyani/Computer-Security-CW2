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

if len(sys.argv) != 2:
    print("You must pick exactly one of the following flags: --relay, --break-heart, --custom")
    sys.exit(1)

if args.relay:
    print("EVE IS ON RELAY MODE")
elif args.break_heart:
    print("EVE IS ON BREAK HEART MODE")
elif args.custom:
    print("EVE IS ON CUSTOM MODE")

print('=========================================')

dialog = Dialog('print')

# establish a socket pretending to be alice
print('PRETENDING TO BE ALICE...')
player1 = 'alice'
alice_socket, alice_aes = setup(player1, BUFFER_DIR, BUFFER_FILE_NAME)
os.rename(BUFFER_DIR + BUFFER_FILE_NAME, BUFFER_DIR + "new_buffer")
print('SOCKETS FOR COMMUNICATION WITH BOB ESTABLISHED!')

# establish a socket pretending to be bob
print('PRETENDING TO BE BOB...')
player2 = 'bob'
bob_socket, bob_aes = setup(player2, BUFFER_DIR, BUFFER_FILE_NAME)
print('SOCKETS FOR COMMUNICATION WITH ALICE ESTABLISHED!')

received_from_alice = receive_and_decrypt(bob_aes, bob_socket) # message from alice

# ======================================= RELAY MODE =======================================
if args.relay:

    encrypt_and_send(received_from_alice, alice_aes, alice_socket)
    dialog.chat('Alice said: "{}"'.format(received_from_alice))

    dialog.info('Message sent! Waiting for reply...')
    received_from_bob = receive_and_decrypt(alice_aes, alice_socket)

    dialog.chat('Bob said: "{}"'.format(received_from_bob))

    encrypt_and_send(received_from_bob, bob_aes, bob_socket)

# ======================================= BREAK-HEART MODE =======================================
elif args.break_heart:

    # Make alice send BAD_MSG instead of NICE_MSG to bob
    to_send = BAD_MSG[player1] 

    encrypt_and_send(to_send, alice_aes, alice_socket)
    dialog.chat('Alice said: "{}"'.format(to_send))

    dialog.info('Message sent! Waiting for reply...')
    received_from_bob = receive_and_decrypt(alice_aes, alice_socket)

    dialog.chat('Bob said: "{}"'.format(received_from_bob))

    encrypt_and_send(received_from_bob, bob_aes, bob_socket)

# ======================================= CUSTOM MODE =======================================
elif args.custom:

    dialog.chat('Alice said: "{}"'.format(received_from_alice))

    # Prompt the user for alice's message
    dialog.prompt('Input what you would like Alice to say to Bob')
    alice_send = input()

    encrypt_and_send(alice_send, alice_aes, alice_socket)

    dialog.info('Message sent! Waiting for reply...')
    received_from_bob = receive_and_decrypt(alice_aes, alice_socket)
    dialog.chat('Bob said: "{}"'.format(received_from_bob))

    # Prompt the user for bob's message
    dialog.prompt('Input what you would like Bob to say to Alice')
    bob_send = input()

    encrypt_and_send(bob_send, bob_aes, bob_socket)


tear_down(alice_socket, BUFFER_DIR, "new_buffer")
tear_down(bob_socket, BUFFER_DIR, BUFFER_FILE_NAME)