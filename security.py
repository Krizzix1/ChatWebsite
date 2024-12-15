import secrets
import hashlib

def gen_salt():
    salt = secrets.token_bytes(16)
    print(salt)
    salt_hash = hashlib.sha256(salt).hexdigest()
    print(salt_hash)
    return salt_hash

def hash_pass(password, salt):
    print(f"Password: {password}, Salt: {salt}, Password + Salt: {password + salt}")
    return hashlib.sha256((password + salt).encode('utf-8')).hexdigest()
