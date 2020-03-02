import hashlib
import itertools
from collections import defaultdict

def hash(s):
    m = hashlib.sha1(s.encode())
    return m.hexdigest()

dd = {}
salts = {}
f = open("rockyou-samples.sha1-salt.txt")
for line in f.readlines():
    c_line = line.rstrip()
    salt = c_line.split('$')[2]
    c_line_cleaned = c_line.split('$')[3]
    if salt in salts:
        salts[salt] += 1
    else:
        salts[salt] = 1

    if c_line_cleaned in dd:
        dd[c_line_cleaned] += 1
    else:
        dd[c_line_cleaned] = 1


common_passwords = ["123456", "12345", "123456789", "password", "iloveyou",
	"princess", "1234567", "rockyou", "12345678", "abc123",
	"nicole", "daniel", "babygirl", "monkey", "lovely",
	"jessica", "654321", "michael", "ashley", "qwerty",
	"111111", "iloveu", "000000", "michelle", "tigger"]



common_passwords_with_salt = {}

for common_password in common_passwords:
    for salt in salts:
        common_passwords_with_salt.setdefault(common_password, [])
        common_passwords_with_salt[common_password].append(hash(salt + common_password))


# common_passwords_hashed = [hash(common_password) for common_password in common_passwords_with_salt]
counter = {}
#print(common_passwords_with_salt['123456'])
for i in dd.keys():
    for key in common_passwords_with_salt.keys():
        for value in common_passwords_with_salt[key]:
            if i == value:
                counter.setdefault(key, 0)
                counter[key] += 1
                print(counter)

wf = open("salt-cracked.txt", "w")
wf.writelines(["{},{}\n".format(counter[h],h) for h in counter])
wf.close()
f.close()



