FROM python:3.9.0

WORKDIR /home/

RUN echo "testing111"

RUN git clone https://github.com/wondora/infogigi.git 

WORKDIR /home/infogigi

RUN pip install -r requirements.txt

RUN pip install gunicorn

RUN pip install mysqlclient

RUN echo "SECRET_KEY = 0lb#yu$t1r8_+0g-yt33@y)ge2(&+4_$r84&hi(7#tz3l^yo21" > .env

EXPOSE 8000

CMD ["bash", "-c", "python manage.py collectstatic --noinput --settings=gshs.settings.deploy && python manage.py migrate --settings=gshs.settings.deploy && gunicorn infogigi.wsgi --bind 0.0.0.0:8000  --settings=gshs.settings.deploy"]