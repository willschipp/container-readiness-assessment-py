## Kserve deployment

### Steps

1. deploy kserve > 0.13
2. create a deployment namespace (e.g. llama-cpp)
3. deploy [runtime](./runtime.yaml) to establish the custom runtime
4. deploy [inference](./inference.yaml) to create an instance