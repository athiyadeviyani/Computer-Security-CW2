import hashlib
import itertools
from collections import defaultdict, Counter
from Cryptodome.Hash import SHA1

def hash(s):
    m = SHA1.new(bytearray(s, 'utf-8')).hexdigest()
    return m

common_passwords = ["123456", "12345", "123456789", "password", "iloveyou",
	"princess", "1234567", "rockyou", "12345678", "abc123",
	"nicole", "daniel", "babygirl", "monkey", "lovely",
	"jessica", "654321", "michael", "ashley", "qwerty",
	"111111", "iloveu", "000000", "michelle", "tigger"]

samples = open("rockyou-samples.sha1-salt.txt")
counts = Counter()

def crack(): 
    print('Checking all hashes...')

    for line in samples.readlines():
        cline = line.rstrip()
        salt = cline.split('$')[2]
        hashed = cline.split('$')[3]

        for password in common_passwords:
            salted_password = salt + password
            if hash(salted_password) == hashed:
                counts.update({password : 1})

    print(counts.items())  

    wf = open("salt-cracked.txt", "w")
    wf.writelines(["{},{}\n".format(count, password) for password, count in counts.items()])
    wf.close()
    samples.close()
            

    # print('Writing file...')
    # with open('salt-cracked2.txt', 'w') as cracked:
    #     for password, count in counts.items():
    #         row = str(count) + ',' + password + '\n'
    #         cracked.write(row)

    print('DONE!')

crack()