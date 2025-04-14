## S3 Testing

### Minio for local


#### Server install

1. download minio `wget https://dl.min.io/server/minio/release/linux-amd64/minio`
2. install `chmod +x minio`
3. run `MINIO_ROOT_USER=admin MINIO_ROOT_PASSWORD=password ./minio server ./data --console-address :9001 &`

#### Client install

1. download the client `curl https://dl.min.io/client/mc/release/linux-amd64/mc \
  --create-dirs \
  -o $HOME/minio-binaries/mc`
2. install `chmod +x $HOME/minio-binaries/mc`

#### setup alias

`./mc alias set myminio http://localhost:9000 admin password`

#### Setup test keys

`./mc admin accesskey create myminio/admin --access-key mytestkey --secret-key mytestsecret`