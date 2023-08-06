from passlib.hash import bcrypt

class Bcrypt:
    @staticmethod
    def create_bcrypt(string: str):
        return bcrypt.hash(string)
    
    @staticmethod
    def verify_bcrypt(string: str, hash: str):
        return bcrypt.verify(string, hash)
