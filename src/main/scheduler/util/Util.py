import hashlib
import base64
import uuid

class Util:
    
    def generate_salt():
        return base64.urlsafe_b64encode(uuid.uuid4().bytes)

    def generate_hash(password, salt):
        t_sha = hashlib.sha512()
        t_sha.update(password+salt)
        hashed_password =  base64.urlsafe_b64encode(t_sha.digest())
        return hashed_password