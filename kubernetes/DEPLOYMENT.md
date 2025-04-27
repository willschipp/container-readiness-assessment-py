## Deployment considerations for K8S

### Order

1. deploy `minio`
2. use external LB to access `minio` and create bucket and access token
3. create `secret` for LLM secret
4. update app deployment yaml with `minio` location and tokens
5. deploy app


### Enhancement for security

- change the admin username/password for `minio`
- set them in a secret / accessible area for admin only