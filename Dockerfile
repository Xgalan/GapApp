FROM python:3.9.16-slim-bullseye as build

# These two environment variables prevent __pycache__/ files.
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /usr/src/app
RUN python -m venv /usr/src/app/venv
ENV PATH="/usr/src/app/venv/bin:$PATH"
COPY setup.py .
RUN apt-get update && apt-get install -y build-essential mariadb-client libmariadb-dev \
    && pip install wheel && pip install --no-cache-dir .

FROM python:3.9.16-slim-bullseye

ARG USER_ID
ARG GROUP_ID

RUN apt-get update && apt-get install -y mariadb-client \
    && rm -rf /var/cache/apt/archives \
    && rm -rf /var/lib/apt/lists/*

RUN getent group ${GROUP_ID} || addgroup --gid $GROUP_ID gap \
    && adduser --disabled-password --gecos '' --uid $USER_ID --gid $GROUP_ID gap \
    && mkdir /usr/src/app \
    && chown ${USER_ID}:${GROUP_ID} /usr/src/app \
    && mkdir -p /srv/databases /srv/fixtures \
    && chown -R ${USER_ID}:${GROUP_ID} /srv/databases \
    && chown -R ${USER_ID}:${GROUP_ID} /srv/fixtures

WORKDIR /usr/src/app

COPY --chown=${USER_ID}:${GROUP_ID} --from=build /usr/src/app/venv ./venv
COPY --chown=${USER_ID}:${GROUP_ID} . .

USER gap 

ENV PATH="/usr/src/app/venv/bin:$PATH"
ENV PYTHONPATH="/usr/src/app/gap:$PYTHONPATH"

ENTRYPOINT [ "/usr/src/app/entrypoint.sh" ]