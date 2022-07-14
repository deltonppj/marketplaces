from passlib.context import CryptContext

CRIPTOR_CONTEXT = CryptContext(schemes=['bcrypt'], deprecated='auto')


def check_hash(password: str, hashed_password: str) -> bool:
    return CRIPTOR_CONTEXT.verify(password, hashed_password)


def hash_generator(password: str) -> str:
    return CRIPTOR_CONTEXT.hash(password)
