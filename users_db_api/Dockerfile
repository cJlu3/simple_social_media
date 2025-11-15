FROM python:3.13-trixie

WORKDIR /app

COPY ./src/ ./src/
COPY ./requirements.txt .

RUN pip install -r requirements.txt

CMD [ "python", "-m", "src.main" ]
