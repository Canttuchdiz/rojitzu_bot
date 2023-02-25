FROM python:3.10-bullseye

COPY requirements.txt /app/

WORKDIR /app

RUN pip install -r requirements.txt

RUN prisma generate

COPY . .

CMD ["python3", "-m", "rojitzu"]
