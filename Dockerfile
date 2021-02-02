FROM python:3.8.5

WORKDIR /home/

RUN echo "testing1333"

RUN git clone https://github.com/wondora/infogigis.git 

WORKDIR /home/infogigis

RUN pip install -r requirements.txt

RUN pip install gunicorn

RUN pip install mysqlclient

EXPOSE 8000

CMD ["bash", "-c", "python manage.py collectstatic --noinput --settings=gshs.settings.deploy && python manage.py migrate --settings=gshs.settings.deploy"]