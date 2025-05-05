FROM python:3.12

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install --default-timeout=100 future
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "backend/app/main.py" ]