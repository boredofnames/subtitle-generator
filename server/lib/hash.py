import hashlib

def get_hashed(data):
    return hashlib.shake_256(data.encode()).hexdigest(5)
