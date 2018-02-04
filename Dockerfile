FROM python:3

WORKDIR /usr/src/app

RUN pip install Pillow
COPY . .
CMD ["python", "tic-tac-toe.py"]
