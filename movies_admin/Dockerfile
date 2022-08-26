FROM python:3.10

WORKDIR /app

ENV DJANGO_SETTINGS_MODULE 'config.settings'

COPY requirements.txt requirements.txt

RUN  pip install --upgrade pip \
     && pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["gunicorn", "config.wsgi:application", "--bind", "0:8000" ]