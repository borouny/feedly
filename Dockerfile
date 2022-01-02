FROM python:3.7

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV ENV=PRODUCTION
RUN mkdir /app
WORKDIR /app
COPY requirements.txt /app/
RUN pip install -r /app/requirements.txt

COPY . /code/
CMD python manage.py migrate
