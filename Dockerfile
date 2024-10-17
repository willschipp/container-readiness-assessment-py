# Build
FROM node:18 as build

WORKDIR /app

COPY frontend/* .

RUN npm install && npm run build

# Runtime
FROM python:3.9-slim as runtime

WORKDIR /app

COPY --from=build build frontend/build

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY server .

# COPY frontend/build .

# set env variables
ENV FLASK_APP=server/server.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_CONFIG=default

EXPOSE 5000

CMD ["flask","run"]
