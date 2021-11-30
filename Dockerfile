FROM python:3.8.12-slim-bullseye

WORKDIR /usr/src/app
COPY . .
RUN pip install --editable .
RUN python ./gap/manage.py makemigrations
RUN python ./gap/manage.py migrate
RUN python ./gap/manage.py collectstatic --no-input

# for creating first superuser you could use:
RUN /bin/bash -c 'cat ./gap/createsuperuser.example | python ./gap/manage.py shell'
RUN /bin/bash -c 'cat ./gap/createuser.example | python ./gap/manage.py shell'

# load users from dumped existing data
#RUN python ./gap/manage.py loaddata users.json

# load fixtures, see content of loaddata.example
#RUN /bin/bash -c './gap/loaddata.example'
ENV PYTHONPATH=/usr/src/app/gap