# minio-aistor-patcher

As Minio changed license terms and trimmed it's open source edition, I created this Docker image

It does what it does.

Example `docker-compose.yml`:

```yaml
services:
  minio:
    build: https://github.com/radioegor146/minio-aistor-patcher.git
    restart: always
    volumes:
      - "./storage:/storage"
    ports:
      - 9000:9000
      - 9001:9001
    command: server /storage
```