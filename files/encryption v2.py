import base64
import zlib
import marshal
import hashlib
import os
import random
import string
import time
from Crypto.Cipher import AES

# 🎨 color codes
R = "\033[91m"
G = "\033[92m"
Y = "\033[93m"
B = "\033[94m"
C = "\033[96m"
W = "\033[0m"

# ⏳ typing animation
def slow(text, delay=0.01):
    for c in text:
        print(c, end="", flush=True)
        time.sleep(delay)
    print()

# 🔄 loading animation
def loading(msg="Processing"):
    for _ in range(3):
        print(f"{Y}{msg}.{W}", end="\r")
        time.sleep(0.3)
        print(f"{Y}{msg}..{W}", end="\r")
        time.sleep(0.3)
        print(f"{Y}{msg}...{W}", end="\r")
        time.sleep(0.3)
    print(" " * 20, end="\r")

# 🔀 random নাম generator
def rand_name(n=8):
    return ''.join(random.choice(string.ascii_letters) for _ in range(n))

# 🔑 hidden key parts
K1 = "nhbd_"
K2 = "secure_"
K3 = "key_123"

def derive_key():
    full = K1 + K2 + K3
    return hashlib.sha256(full.encode()).digest()

# 🔐 multi-layer encryption (UNCHANGED)
def encrypt(code):
    key = derive_key()

    compiled = compile(code, "<protected>", "exec")
    marshaled = marshal.dumps(compiled)
    compressed = zlib.compress(marshaled)

    cipher1 = AES.new(key, AES.MODE_GCM)
    ct1, tag1 = cipher1.encrypt_and_digest(compressed)
    layer1 = cipher1.nonce + tag1 + ct1

    cipher2 = AES.new(key, AES.MODE_GCM)
    ct2, tag2 = cipher2.encrypt_and_digest(layer1)
    final = cipher2.nonce + tag2 + ct2

    return base64.b64encode(final).decode()

# 🧠 loader builder (UNCHANGED)
def build_loader(enc_data):
    v1, v2, v3, v4 = rand_name(), rand_name(), rand_name(), rand_name()

    return f'''
import base64,zlib,marshal,hashlib,os,sys
from Crypto.Cipher import AES

def {rand_name()}():
    return "Nothing to see here"

if sys.gettrace():
    exit()

K1="nhbd_";K2="secure_";K3="key_123"

def {v1}():
    return hashlib.sha256((K1+K2+K3).encode()).digest()

{v2}=base64.b64decode("{enc_data}")

def {v3}(d):
    n,t,c=d[:16],d[16:32],d[32:]
    k={v1}()
    x=AES.new(k,AES.MODE_GCM,nonce=n)
    return x.decrypt_and_verify(c,t)

{v4}={v3}({v2})
{v4}={v3}({v4})

code_obj=marshal.loads(zlib.decompress({v4}))

exec(code_obj)

cur=os.path.abspath(__file__)
fld=os.path.dirname(cur)

for f in sorted(os.listdir(fld)):
    if not f.endswith(".py"): continue
    p=os.path.join(fld,f)
    if os.path.abspath(p)==cur: continue
    try:
        exec(compile(open(p).read(),f,'exec'))
    except:
        pass
'''

# 🚀 MAIN (UI enhanced only)
if __name__ == "__main__":
    os.system("cls" if os.name == "nt" else "clear")

    slow(f"{C}===================================={W}")
    slow(f"{G}   🔐 NHBD ENCRYPTION TOOL{W}")
    slow(f"{B}   Developer: noobxvau{W}")
    slow(f"{C}===================================={W}\n")

    folder = os.getcwd()

    py_files = [
        f for f in os.listdir(folder)
        if f.endswith(".py") and f != os.path.basename(__file__)
    ]

    if not py_files:
        slow(f"{R}❌ No Python files found{W}")
        exit()

    slow(f"{Y}📂 Available Python Files:\n{W}")

    for i, file in enumerate(py_files, 1):
        print(f"{C}[{i}] {G}{file}{W}")

    while True:
        try:
            choice = int(input(f"\n{Y}Select file number ➤ {W}"))
            if 1 <= choice <= len(py_files):
                selected_file = py_files[choice - 1]
                break
            else:
                slow(f"{R}Invalid choice!{W}")
        except:
            slow(f"{R}Enter a valid number!{W}")

    slow(f"\n{B}🔄 Encrypting: {selected_file}{W}")
    loading("Encrypting")

    with open(selected_file, "r") as f:
        code = f.read()

    enc = encrypt(code)
    loader = build_loader(enc)

    base_name = os.path.splitext(selected_file)[0]
    output_name = f"{base_name}_nhbd_encrypted.py"

    with open(output_name, "w") as f:
        f.write(loader)

    slow(f"\n{G}✅ Done Successfully!{W}")
    slow(f"{C}🔐 Protected File: {output_name}{W}\n")