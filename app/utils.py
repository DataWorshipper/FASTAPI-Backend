from passlib.context import CryptContext
pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto",
    argon2__memory_cost=19456,
    argon2__time_cost=2,
    argon2__parallelism=1,
)
def hash(password:str):
    return pwd_context.hash(password)

def  verify(plain_password,hashed_password):
    return pwd_context.verify(plain_password,hashed_password)
