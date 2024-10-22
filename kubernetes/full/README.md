## Components

- minio (storage s3)
- llama.cpp container (Q8 for inference)
- nginx reverse proxy/ingress


### Minio

https://min.io/docs/minio/kubernetes/upstream/index.html


### Llama.cpp

`quay.io/w_schipp/model_work:Q8`

### Nginx

[Nginx](./nginx/README.md)


## Build Installations

1. deploy k8s to a single-VM [oss_k8s](./oss_k8s/RUNBOOK.md)
   - include OSS k8s
   - include kserve
2. deploy minio
   - `kubectl get nodes --show-labels`
   - install `mc` on server
   ```shell
    curl https://dl.min.io/client/mc/release/linux-amd64/mc \
    --create-dirs \
    -o $HOME/minio-binaries/mc

    chmod +x $HOME/minio-binaries/mc
    export PATH=$PATH:$HOME/minio-binaries/

    mc --help   
   ```
   - login `mc mb <bucket-name>`
   - `mc policy set <bucket-name> public-read`
   - ```json
    {
    "CORSRules": [
        {
        "AllowedOrigins": ["*"],
        "AllowedMethods": ["GET", "PUT", "DELETE"],
        "AllowedHeaders": ["*"],
        "ExposeHeaders": ["ETag", "Content-Length"]
        }
    ]
    }
   ```
   - `mc cors set <bucket-name> cors.json`
   - edit `minio.conf`
     ```
     [server]
        public_address = ":9000" # adjust the port if needed
     ```
3. deploy llama.cpp (kserve)
   - custom-runtime
   - custom inference (Q8)
4. deploy nginx
   - reverse proxy for minio
   - reverse proxy for llama.cpp
5. deploy app