ARG OS_IMAGE=archlinux:latest

FROM ${OS_IMAGE} as base

RUN pacman -Syy

RUN pacman -Sy --noconfirm archlinux-keyring && \
    pacman -Syu --noconfirm

RUN pacman -Sy --noconfirm base-devel wget sudo

RUN wget https://www.python.org/ftp/python/3.12.0/Python-3.12.0.tgz && \
    tar -xvf Python-3.12.0.tgz && \
    cd Python-3.12.0 && \
    ./configure --enable-optimizations && \
    make && \
    make install && \
    cd .. && \
    rm -rf Python-3.12.0 && \
    rm Python-3.12.0.tgz && \
    echo "export PATH=\"/usr/local/bin:\$PATH\"" >> /etc/profile.d/python_custom.sh

RUN ln -s /usr/local/bin/python3 /usr/local/bin/python && \
    ln -s /usr/local/bin/pip3 /usr/local/bin/pip

RUN python3 -m ensurepip --upgrade

RUN python3 -m pip install poetry

RUN mkdir /app

WORKDIR /app

COPY ./ /app/

# Local split
FROM base as local-image

RUN python3 -m poetry config virtualenvs.create false \
    && python3 -m poetry install --no-root --no-interaction --no-ansi --compile

EXPOSE 8000

RUN chmod +x /app/scripts/start/local.sh

ENTRYPOINT ["/app/scripts/start/local.sh"]

# Dev split
FROM base as dev-image

RUN python3 -m poetry config virtualenvs.create false \
    && python3 -m poetry install --no-root --without dev --no-interaction --no-ansi --compile

EXPOSE 8000

RUN chmod +x /app/scripts/dev/local.sh

ENTRYPOINT ["/app/scripts/start/dev.sh"]

# Prod split
FROM base as prod-image

RUN python3 -m poetry config virtualenvs.create false \
    && python3 -m poetry install --no-root --without dev --no-interaction --no-ansi --compile

EXPOSE 8000

RUN chmod +x /app/scripts/start/prod.sh

ENTRYPOINT ["/app/scripts/start/prod.sh"]
