# Build
FROM node:slim as build

WORKDIR /app

COPY frontend/. ./

# install and build

RUN npm install && npm run build

# Runtime
FROM python:3.9-slim as runtime

WORKDIR /app

RUN mkdir /app/frontend

COPY --from=build /app/build /app/frontend/build/.

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir /app/server

COPY server /app/server/.

# set env variables
ENV FLASK_APP=/app/server/server.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_CONFIG=default

EXPOSE 5000

CMD ["flask","run"]