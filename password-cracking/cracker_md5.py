import hashlib
import itertools
from collections import defaultdict

def hash(s):
    m = hashlib.md5(s.encode())
    return m.hexdigest()

dd = {}
f = open("rockyou-samples.md5.txt")
for line in f.readlines():
    c_line = line.rstrip()
    if c_line in dd:
        dd[c_line] += 1
    else:
        dd[c_line] = 1

def crack():
    print("Cracking...")
    cs = "0123456789abcdefghijklmnopqrstuvwxyz"
    possible_passwords = [a+b+c+d+e for a,b,c,d,e in itertools.product(cs, repeat=5)]
    hm = {}
    for possible_password in possible_passwords:
        hashed = hash(possible_password)
        if hashed in dd:
            hm[possible_password] = dd[hashed]

    print("DONE!")

    wf = open("md5-cracked.txt", "w")
    wf.writelines(["{},{}\n".format(hm[h],h) for h in hm])
    wf.close()
    f.close()
    return

crack()

