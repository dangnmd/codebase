import hashlib
import os
import sys

curr_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(curr_dir)
sys.path.append(os.path.join(curr_dir, '../'))

from common.crypt import *

# gen app key
print(binascii.hexlify(random_bytes(32).encode())[:64])

# gen django secret
print((''.join([random.choice('abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)') for _ in range(50)])))