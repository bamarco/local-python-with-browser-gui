## Base System
FROM node:22@sha256:69e667a79aa41ec0db50bc452a60e705ca16f35285eaf037ebe627a65a5cdf52

#FROM python:3.11.9-slim@sha256:80bcf8d243a0d763a7759d6b99e5bf89af1869135546698be4bf7ff6c3f98a59

# Install python/pip
ENV PYTHONUNBUFFERED=1
RUN apt-get update && apt-get install -y --no-install-recommends python3 python3-pip python3.11-venv

## Copy Files (check .dockerignore for files not copied)
COPY ./ /srv/app/

## Build Frontend
RUN cd /srv/app/frontend && npm ci
RUN cd /srv/app/frontend && npm run build

## Python 3.11 virtual environment
ENV VIRTUAL_ENV=/opt/venv
RUN python3.11 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

## Install Backend Dependencies
RUN cd /srv/app && pip install -r requirements.txt

## Deployment Server
WORKDIR /srv/app
CMD ["python", "app.py"]
EXPOSE 5000
