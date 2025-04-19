## Setup a 'local' demo


### Setup steps
1. minio
2. update settings.toml with keys for minio


### Minio

`docker run --name minios3 -p 9000:9000 -p 9001:9001 -d quay.io/minio/minio server ./data --console-address ":9001"`

`minioadmin:minioadmin`

### Using Gemini