import bcrypt
import jwt
import datetime

SECRET_KEY = "75017fe6e3bf084e3056c2ddb9d7e6fbd0d66f2cfa8b0502608fa2c9a79d114f"

def hash_heslo(heslo: str) -> bytes:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(str.encode(heslo), salt)
    return hashed


def porovnej_heslo(heslo_k_porovnani: bytes, hash_heslo_z_db: bytes) -> bool:
    return bcrypt.checkpw(heslo_k_porovnani, hash_heslo_z_db)


def token_respose(jmeno: str) -> dict:
    obsah = {
        "jmeno": jmeno,
        "exp": datetime.datetime.now(tz=datetime.timezone.utc).timestamp() + 5, #14 * 24 * 60 * 60
    }
    encoded_jwt = jwt.encode(obsah, SECRET_KEY)
    return {"token": encoded_jwt}

def token_decode(token: str) -> str:
    try:
        madar = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except:
        return ""
    return madar["jmeno"]