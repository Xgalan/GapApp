FROM python:3.8.13-slim-bullseye as build

# These two environment variables prevent __pycache__/ files.
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /usr/src/app
RUN python -m venv /usr/src/app/venv
ENV PATH="/usr/src/app/venv/bin:$PATH"
COPY setup.py .
RUN pip install --no-cache-dir --editable .


FROM python:3.8.13-slim-bullseye@sha256:92331358d341594de3857397796335d6e1e26fca1230709e439a415624792c87

ARG USER_ID
ARG GROUP_ID

RUN getent group ${GROUP_ID} || addgroup --gid $GROUP_ID gap \
    && adduser --disabled-password --gecos '' --uid $USER_ID --gid $GROUP_ID gap \
    && mkdir /usr/src/app \
    && chown ${USER_ID}:${GROUP_ID} /usr/src/app \
    && mkdir -p /srv/databases \
    && chown -R ${USER_ID}:${GROUP_ID} /srv/databases

WORKDIR /usr/src/app

COPY --chown=${USER_ID}:${GROUP_ID} --from=build /usr/src/app/venv ./venv
COPY --chown=${USER_ID}:${GROUP_ID} . .

USER gap 

ENV PATH="/usr/src/app/venv/bin:$PATH"

ENV PYTHONPATH="/usr/src/app/gap:$PYTHONPATH"

ENTRYPOINT [ "/usr/src/app/entrypoint.sh" ]