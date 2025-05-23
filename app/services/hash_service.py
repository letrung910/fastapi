from passlib.context import CryptContext

bcrypt_context = CryptContext(schemes=['bcrypt'])

def get_password_hash(password):
    hash_password = bcrypt_context.hash(password)
    print(hash_password)
    return hash_password


def verify_password(plain_password, hashed_password):
    return bcrypt_context.verify(plain_password, hashed_password)

