FROM python:3.8.5

RUN mkdir /code
COPY requirements.txt /code
COPY . /code
WORKDIR /code
RUN pip3 install -r requirements.txt
