import bcrypt
from abc import abstractmethod, ABC
from time import perf_counter
from typing import Union

from others.settings import TOKEN_SECRET


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
        self.__salt = b"$2b$12$IfWmvy0xVWeuRZ/6tobhe."
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


class Token(HashedData):
    def __init__(self):
        self._string = bcrypt.gensalt()
        self._secret = TOKEN_SECRET.encode()
        self._token_hash = self._hash_data()

    @abstractmethod
    def _hash_data(self):
        pass

    def __eq__(self, other: Union[str, "Token"]) -> bool:
        if isinstance(other, Token):
            return self.hash == other.hash
        if isinstance(other, str):
            return self.hash == other
        return False

    @property
    def hash(self) -> str:
        return self._token_hash


class RefreshToken(Token):
    def __init__(self):
        super().__init__()

    def _hash_data(self):
        result = self._string
        start = perf_counter()
        result = bcrypt.hashpw(self._secret, result)
        print("Итог:", perf_counter() - start)
        return result.decode()


class AccessToken(Token):
    def __init__(self):
        super().__init__()

    def _hash_data(self):  # переделать потомучто фигню возвращает
        result = self._string
        start = perf_counter()
        result = bcrypt.hashpw(self._secret, result)
        result = result.decode() + "." + bcrypt.hashpw(self._secret, result).decode()
        print("Итог:", perf_counter() - start)
        return result


# class Device(HashedData):
#     ...


if __name__ == "__main__":
    password = Password("12345689893432")
    psw = Password("12345689893432")
    print(password.hash)
    print(password == "$2b$12$IfWmvy0xVWeuRZ/6tobhe..mrm6Kv9D42wzfRqUDHVPPBXVOaDVhi")
    print(password == psw)
    print(len(password.hash))
    token = RefreshToken()
    token_2 = AccessToken()
    print(f"Access: {token_2.hash, len(token_2.hash)}")
    print(f"Refresh: {token.hash, len(token.hash)}")
    print(token_2 == '$2b$12$liyfhEdVa3H1YqsWDz4AA.sOydTA5kGvjJKtA0cpVU6g/vIFq4ftu.$2b$12$liyfhEdVa3H1YqsWDz4AA.sOydTA5kGvjJKtA0cpVU6g/vIFq4ftu')
