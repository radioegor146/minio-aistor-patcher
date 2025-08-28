FROM quay.io/minio/aistor/minio:latest AS minio

FROM python:3.14-alpine AS patcher
WORKDIR /patcher
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
COPY /bin/minio minio --from minio
RUN sh generate-keys.sh
RUN python3 replace-key.py minio minio-patched new-public.pem
RUN python3 generate-license new-private.pem minio.license

FROM quay.io/minio/aistor/minio:latest
COPY /patcher/minio-patched /bin/minio --from patcher
COPY /patcher/minio.license /minio.license --from patcher
ENV MINIO_LICENSE=/minio.license