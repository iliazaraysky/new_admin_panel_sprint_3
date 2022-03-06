FROM python:3.8.5
RUN mkdir /code
COPY requirements.txt /code
RUN pip install --upgrade pip && pip install -r /code/requirements.txt
COPY . /code
WORKDIR /code/app/
CMD gunicorn config.wsgi:application --bind 0.0.0.0:8000
RUN mkdir static
RUN python manage.py collectstatic
