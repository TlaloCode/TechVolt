ARG PYTHON_VERSION=3.9-slim-bullseye
FROM python:${PYTHON_VERSION} as awscli

# Versions: https://pypi.python.org/pypi/awscli#downloads
ENV AWS_CLI_VERSION 1.16.140

# Install required system dependencies
RUN apt-get update \
  && pip3 --no-cache-dir install awscli==${AWS_CLI_VERSION} \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*


WORKDIR /data

COPY ./compose/local/aws/maintenance /usr/local/bin/maintenance
COPY ./compose/local/postgres/maintenance/_sourced /usr/local/bin/maintenance/_sourced

RUN chmod +x /usr/local/bin/maintenance/*

RUN mv /usr/local/bin/maintenance/* /usr/local/bin \
    && rmdir /usr/local/bin/maintenance
