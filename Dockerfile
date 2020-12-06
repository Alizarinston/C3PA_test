FROM python:3.8

RUN mkdir -p /usr/src/app

WORKDIR /usr/src/app

COPY . /usr/src/app
RUN pip install --no-cache-dir -r requirements.txt && python manage.py makemigrations && python manage.py migrate --run-syncdb

EXPOSE 8000

CMD ["uvicorn", "C3PA_test.asgi:application", "--host", "0.0.0.0"]
