## LLM Deployment

To run the Container Readiness Assessment Platform, an LLM is used to assess the build files.
Included are Kubernetes container deployment examples for CodeLlama-7B-Instruct deployed using Llama.cpp.

The OCI used is a custom image that runs the latest version of Llama-server (llama.cpp) inside an Ubuntu container.
It has two version; 2Q_K.gguf "latest" tag, and Q8_0.gguf "Q8" tag.  The models are embedded in the container for easier deployment.

### Requirements

CPU only

### Deployment Options

There are 2 deployment examples; standard [Kubernetes](./standalone/README.md) container and [Kserve](./kserve/README.md)

