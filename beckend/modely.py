from dataclasses import dataclass


@dataclass
class LoginARegisterBody:  # zatim dohromady
    username: str
    password: str
    

### DATABAZE ###


@dataclass
class User:
    id: int
    jmeno: str
    hash_heslo: bytes
    aktivni: bool
