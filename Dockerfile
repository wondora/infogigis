FROM python:3.8.5

WORKDIR /home/

RUN echo "testing1663"

RUN git clone https://github.com/wondora/infogigis.git 

WORKDIR /home/infogigis

RUN pip install -r requirements.txt

RUN echo "SECRET_KEY=0lb#yu$t1r8_+0g-yt33@y)ge2(&+4_$r84&hi(7#tz3l^yo21" > .env

RUN python manage.py migrate

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]