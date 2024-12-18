import secrets
import hashlib
from Crypto.PublicKey import RSA


def gen_salt():
    salt = secrets.token_bytes(16)
    print(salt)
    salt_hash = hashlib.sha256(salt).hexdigest()
    print(salt_hash)
    return salt_hash


def hash_pass(password, salt):
    print(f"Password: {password}, Salt: {salt}, Password + Salt: {password + salt}")
    return hashlib.sha256((password + salt).encode('utf-8')).hexdigest()


def gen_secret_key():
    return secrets.token_hex(16)


def gen_key_pair():
    keys = RSA.generate(2048)

    private_key = keys.export_key()
    public_key = keys.publickey().export_key()

    return public_key, private_key