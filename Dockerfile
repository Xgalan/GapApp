FROM python:3.8.13-slim-bullseye as build

WORKDIR /usr/src/app
RUN python -m venv /usr/src/app/venv
ENV PATH="/usr/src/app/venv/bin:$PATH"
COPY setup.py .
RUN pip install --no-cache-dir --editable .


FROM python:3.8.13-slim-bullseye@sha256:92331358d341594de3857397796335d6e1e26fca1230709e439a415624792c87

RUN useradd --no-create-home --shell /bin/false --system --user-group gap
RUN mkdir /usr/src/app && chown gap:gap /usr/src/app
WORKDIR /usr/src/app

COPY --chown=gap:gap --from=build /usr/src/app/venv ./venv
COPY --chown=gap:gap . .

USER gap 

ENV PATH="/usr/src/app/venv/bin:$PATH"
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
ENV PYTHONPATH="/usr/src/app/gap:$PYTHONPATH"
ENTRYPOINT ["gunicorn", "--worker-tmp-dir", "/dev/shm", "--config", "./gap/gunicorn.conf.py", "gap.wsgi:application"]
