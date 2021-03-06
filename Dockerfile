FROM python:3.8.5

WORKDIR /home/

RUN echo "testing222211"

RUN git clone https://github.com/wondora/infogigis.git 

WORKDIR /home/infogigis

RUN pip install -r requirements.txt

RUN pip install mysqlclient

EXPOSE 8000

CMD ["bash", "-c", "python manage.py collectstatic --noinput --settings=gshs.settings.deploy && python manage.py migrate --settings=gshs.settings.deploy && gunicorn mysite.wsgi --env DJANGO_SETTINGS_MODULE=gshs.settings.deploy --bind 0.0.0.0:8000"]