FROM tiangolo/meinheld-gunicorn:python3.8

COPY ./gap /app
ADD secrets.json /app/secrets.json
ADD ./assets /app/assets
COPY setup.py setup.py
RUN /bin/bash -c 'rm /app/main.py'
RUN /bin/bash -c 'pip install --editable .'
RUN /bin/bash -c './manage.py makemigrations'
RUN /bin/bash -c './manage.py migrate'
RUN /bin/bash -c './manage.py collectstatic --no-input'
