FROM python:buster

RUN mkdir /src
RUN mkdir /data
COPY src /src
COPY data /data
ADD ./requirements.txt /

RUN pip install -r requirements.txt

WORKDIR /src
CMD ["python3", "useractivity_app.py"]