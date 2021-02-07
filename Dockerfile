FROM python:3.8.2-slim

ENV APP_HOME /app
WORKDIR ${APP_HOME}

# Install Ubuntu dependencies
# libopencv-dev = opencv dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
        # python3-setuptools \
        # python3-pip \
        # python3-dev \
        # python3-venv \
        # python3-urllib3 \
        stockfish \
        && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip install chess flask

COPY . ./

# EXPOSE 5000

CMD ["python", "flask-app.py"]