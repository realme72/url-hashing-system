import hashlib

def generate_hash(url):
    hash_object = hashlib.md5(url.encode())
    return hash_object.hexdigest()[:6]
