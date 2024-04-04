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
    number_of_wins: int
    number_of_games: int
