FROM python:3.8.5

WORKDIR /home/

RUN git clone https://github.com/wondora/infogigis.git 

WORKDIR /home/infogigis

RUN pip install -r requirements.txt

RUN echo "testing"

RUN echo "SECRET_KEY=0lb#yu$t1r8_+0g-yt33@y)ge2(&+4_$r84&hi(7#tz3l^yo21" > .env

RUN python manage.py migrate

EXPOSE 8000

CMD ["gunicorn", "info.wsgi", "--bind", "0.0.0.0:8000"]