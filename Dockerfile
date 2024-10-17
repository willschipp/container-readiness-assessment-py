# Build
FROM node:18 as build

WORKDIR /app

COPY frontend/package.json ./

RUN npm install

COPY frontend/* .

RUN npm run build


# Runtime
FROM python:3.9-slim as runtime

WORKDIR /app

COPY --from=build frontend/build frontend/build

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
