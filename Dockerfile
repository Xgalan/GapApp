FROM tiangolo/uvicorn-gunicorn:python3.8

COPY ./gap /app
COPY setup.py setup.py
RUN /bin/bash -c 'rm /app/main.py'
RUN /bin/bash -c 'pip install --editable .'
RUN /bin/bash -c './manage.py makemigrations'
RUN /bin/bash -c './manage.py migrate'

# for creating first superuser you could use:
#RUN /bin/bash -c 'cat createsuperuser.example | ./manage.py shell'
#RUN /bin/bash -c 'cat createuser.example | ./manage.py shell'

# load users from dumped existing data
RUN /bin/bash -c './manage.py loaddata users.json'

RUN /bin/bash -c './manage.py collectstatic --no-input'

# load fixtures, see content of loaddata.example
RUN /bin/bash -c './loaddata.example'
