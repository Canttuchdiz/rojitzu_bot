FROM python:3.10-bullseye

COPY requirements.txt /app/

WORKDIR /app

RUN pip install -r requirements.txt

RUN sudo prisma generate

RUN sudo prisma db push

COPY . .

CMD ["python3", "-m", "rojitzu"]
