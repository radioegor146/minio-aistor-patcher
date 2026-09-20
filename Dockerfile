FROM quay.io/minio/aistor/minio@sha256:107cf2014a9583c74c11e3cdbd6903d89c2244355886b89ce532f4ecae9c23f3 AS minio

FROM python:3.13-alpine AS patcher
RUN apk add openssl
WORKDIR /patcher
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
COPY --from=minio /bin/minio minio
RUN sh generate-keys.sh
RUN python3 replace-key.py minio minio-patched new-public.pem
RUN python3 generate-license.py new-private.pem minio.license

FROM quay.io/minio/aistor/minio@sha256:107cf2014a9583c74c11e3cdbd6903d89c2244355886b89ce532f4ecae9c23f3
COPY --from=patcher /patcher/minio-patched /bin/minio
RUN chmod +x /bin/minio
COPY --from=patcher /patcher/minio.license /minio.license
ENV MINIO_LICENSE=/minio.license