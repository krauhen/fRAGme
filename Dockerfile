FROM python:3.10.6-slim-bullseye

WORKDIR /tmp

RUN pip install --no-cache-dir --upgrade pip

RUN apt update -y
RUN apt upgrade -y

# Install curl for healtcheck
RUN apt install curl -y

# Build sqlite3 for chroma with version >=3.35.0
RUN apt install wget -y
RUN apt install build-essential -y
RUN wget https://sqlite.org/2021/sqlite-autoconf-3350100.tar.gz && \
    tar xvfz sqlite-autoconf-3350100.tar.gz && \
    cd sqlite-autoconf-3350100 && \
    ./configure && \
    make && \
    make install && \
    ldconfig && \
    cd .. && \
    rm -rf sqlite-autoconf-3350100 sqlite-autoconf-3350100.tar.gz

COPY . .
RUN pip install .

RUN chmod +x /tmp/entrypoint.sh

CMD ["/tmp/entrypoint.sh"]