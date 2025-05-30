import bcrypt
from abc import abstractmethod, ABC
from time import perf_counter
from typing import Union
import random

from backend.app.others.settings import PASSWORD_SECRET
from backend.database.creation import db, Profile, Token


# Declaring our password

# longs = []
# # Adding the salt to password
# salt = b'$2b$12$IfWmvy0xVWeuRZ/6tobhe.'
# # Hashing the password
# password = b'GeekPassword'
# for _ in range(10):
#     password = bcrypt.gensalt()
#     start = perf_counter()
#     for _ in range(attempts):
#         password = bcrypt.hashpw(password, salt)
#     result = perf_counter()-start
#     longs.append(result)
#     print("Итог:", result)
#
# print("Максимальная: ", max(longs))


class HashedData(ABC):
    @abstractmethod
    def _hash_data(self):
        pass

    @abstractmethod
    def __eq__(self, other):
        pass

    @property
    def hash(self):
        pass


class Password(HashedData):
    def __init__(self, password_string: str):
        self.__attempts = 5
        self.__salt = PASSWORD_SECRET.encode()
        self.__password_string = password_string.encode()
        self.__password_hash = self._hash_data()

    def _hash_data(self) -> str:
        password = self.__password_string
        start = perf_counter()
        for _ in range(self.__attempts):
            password = bcrypt.hashpw(password, self.__salt)
        print("Итог:", perf_counter() - start)
        return password.decode()

    def __eq__(self, other: Union[str, "Password"]) -> bool:
        if isinstance(other, Password):
            return self.hash == other.hash
        if isinstance(other, str):
            return self.hash == other
        return False

    @property
    def hash(self) -> str:
        return self.__password_hash

    @property
    def start_string(self) -> str:
        return self.__password_string.decode()


class TokenBase(HashedData):
    def __init__(self):
        self._salt = bcrypt.gensalt()
        self._string = str(random.randint(1, 1000000)).encode()
        self._token_hash = self._hash_data()

    @abstractmethod
    def _hash_data(self) -> str:
        pass

    def __eq__(self, other: Union[str, "TokenBase"]) -> bool:
        if isinstance(other, TokenBase):
            return self.hash == other.hash
        if isinstance(other, str):
            return self.hash == other
        return False

    @property
    def hash(self) -> str:
        return self._token_hash


class AccessToken(TokenBase):
    def __init__(self):
        super().__init__()

    def _hash_data(self) -> str:
        start = perf_counter()
        buffer_result = bcrypt.hashpw(self._string, self._salt)
        buffer_salt = bcrypt.gensalt()
        result = (
            bcrypt.hashpw(buffer_result, self._salt).decode()
            + bcrypt.hashpw(
                ("findfs" + self._salt.decode() + self._string.decode()).encode(),
                buffer_salt,
            ).decode()
        )
        print("Итог:", perf_counter() - start)
        return result


def get_profile(token: str) -> Profile:
    u_id = db.session.query(Token).filter(Token.token == token).first().user_id
    return db.session.query(Profile).filter(Profile.user_id == u_id).first()


if __name__ == "__main__":
    # password = Password("12345689893432")
    # psw = Password("12345689893432")
    # print(password.hash)
    # print(password == "$2b$12$IfWmvy0xVWeuRZ/6tobhe..mrm6Kv9D42wzfRqUDHVPPBXVOaDVhi")
    # print(password == psw)
    # print(len(password.hash))
    # token = RefreshToken()
    # token_2 = AccessToken()
    # print(f"Access: {token_2.hash, len(token_2.hash)}")
    # print(f"Refresh: {token.hash, len(token.hash)}")
    # print(
    #     token_2
    #     == "$2b$12$liyfhEdVa3H1YqsWDz4AA.sOydTA5kGvjJKtA0cpVU6g/vIFq4ftu.$2b$12$liyfhEdVa3H1YqsWDz4AA.sOydTA5kGvjJKtA0cpVU6g/vIFq4ftu"
    # )
    print(Password("1234").hash)
    print(Password("12345").hash)
    print(Password("1234").start_string)
