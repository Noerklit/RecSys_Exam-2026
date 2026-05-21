FROM python:buster

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./src ./src
RUN mkdir /data

WORKDIR /app/src
CMD ["python", "feedback_app.py"]