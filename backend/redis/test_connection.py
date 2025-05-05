import redis

if __name__ == "__main__":
    r = redis.Redis(host="localhost", port=6379, db=0)

    try:
        info = r.info()
        print(info["redis_version"])
        response = r.ping()
        if response:
            print("Подключение успешно!")
        else:
            print("Не удалось подключиться к Redis.")
    except redis.exceptions.RedisError as e:
        print(f"Ошибка: {e}")
