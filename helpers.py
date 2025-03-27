import bcrypt
from time import perf_counter
from typing import Union


attempts = 6
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


class Password:
    def __init__(self, password_string):
        self.__attempts = 5
        self.__salt = b'$2b$12$IfWmvy0xVWeuRZ/6tobhe.'
        self.__password_string = password_string.encode()
        self.__password_hash = self.__hash_pswd()


    def __hash_pswd(self) -> str:
        password = self.__password_string
        start = perf_counter()
        for _ in range(attempts):
            password = bcrypt.hashpw(password, self.__salt)
        print("Итог:", perf_counter() - start)
        return password.decode()

    def __eq__(self, other: Union[str, 'Password']) -> bool:
        if isinstance(other, Password):
            return self.hash == other.hash
        if isinstance(other, str):
            return self.hash == other
        return False

    @property
    def hash(self) -> str:
        return self.__password_hash




if __name__ == "__main__":
    password = Password("12345689893432")
    psw = Password("12345689893432")
    print(password.hash)
    print(password == "$2b$12$IfWmvy0xVWeuRZ/6tobhe..mrm6Kv9D42wzfRqUDHVPPBXVOaDVhi")
    print(password == psw)
    print(len(password.hash))