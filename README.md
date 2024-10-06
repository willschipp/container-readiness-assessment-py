
# **C**ontainer **R**eadiness **A**ssessment **P**latform

## What Is It?

Goal: use Large Language Models to accelerate assessment of application code as to whether or not it can be deployed to Kubernetes.  If an application is found to be runnable as a container, provide both the containerization (e.g. Dockerfile) and kubernetes deployment files.

## What It Is Not

- Doesn't propose architectural changes to the application to work on kubernetes
- Doesn't do a full code assessment on the application --> the assumption is the application currently works based on the build file

## How it works

User is asked to fill out a brief form including selecting application language and copy and paste the build file in.  This then creates an "order ID" that the user can track the progress.

In the backgound, a 4 step job is started.
1) can the app run standalone in a container?
2) if it can, create a Dockerfile for it
3) now create a deployment.yaml for it
4) finally, create a service.yaml for it

Once the 4 steps are complete, the user, tracking the progress via the "order ID", can download the 4 generated files.  The intention is that these can be used to form the basis of deploying their app to Kubernetes.

## Under the Covers

- preserves job progress and state in external files --> S3-like object store
- uses Gemini (cloud) or codellama (ollama - local) as the target model
- comprises of a python flask backend with a react frontend
- development done using minio as the s3 backend


## Build Elements

### Front end
1. `rm -rf node_modules`
2. `npm i`
3. `npm run start` --> dev server

### LLM

Gemini API key

### S3 Server

Minio Server
`MINIO_ROOT_USER=admin MINIO_ROOT_PASSWORD=password minio server /mnt/data --console-address ":9001"`