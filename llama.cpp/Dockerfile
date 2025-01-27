# build from centos
FROM quay.io/centos/centos:stream9 as builder

RUN yum install gcc-c++ python3-pip cmake -y

RUN dnf -y install gcc make automake git llvm-toolset gcc-gfortran

RUN dnf group install "Development Tools"

WORKDIR /app

RUN git clone https://github.com/ggerganov/llama.cpp

WORKDIR /app/llama.cpp

# RUN cmake -S . -B build -DCMAKE_BUILD_TYPE=Release -DLLAMA_CURL=ON -DGGML_NATIVE=OFF -DGGML_BACKEND_DL=ON -DGGML_CPU_ALL_VARIANTS=ON -DBUILD_SHARED_LIBS=OFF
RUN cmake -S . -B build -DCMAKE_BUILD_TYPE=Release -DGGML_NATIVE=OFF -DGGML_BACKEND_DL=ON -DGGML_CPU_ALL_VARIANTS=ON

RUN cmake --build build -j $(nproc)

RUN mkdir -p /app/lib && \
    find build -name "*.so" -exec cp {} /app/lib \;

RUN mkdir -p /app/full \
    && cp build/bin/* /app/full \
    && cp *.py /app/full \
    && cp -r gguf-py /app/full \
    && cp -r requirements /app/full \
    && cp requirements.txt /app/full \
    && cp .devops/tools.sh /app/full/tools.sh



