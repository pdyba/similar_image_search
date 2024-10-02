# similar images API

## Architecture

nginx -> backend
backend -> milvus (db)
backend -> redis (cache)

## Usage
1. `make up`
2. Backend, JSON based web API based on OpenAPI: `http://localhost/v1/`
3. Automatic interactive documentation with Swagger UI (from the OpenAPI backend): `http://localhost/docs`

There is no frontend at the moment.

## Backend local development, additional details

### General workflow
See the [Makefile](/Makefile) to view available commands.

### Nginx
The Nginx webserver acts like a web proxy, or load balancer rather. Incoming requests can get proxy passed to various upstreams eg. `/:service1:8001,/static:service2:8002`

### Image Data sets
There is simplified e2e test in tests directory which uses sample data from tests (prepared for integration tests).

There is larger data set in root dir of the project downloaded from:
```bash
$ wget https://github.com/milvus-io/pymilvus-assets/releases/download/imagedata/reverse_image_search.zip
$ unzip -q reverse_image_search.zip -d reverse_image_search
```

You can inser that collection easly. 
Please note we will use the JPEG images only from the "reverse_image_search/train" to build the database. 
There will be about 1000 images.

```bash
$ python ./dev/bulk_insert.py reverse_image_search/train
```

### Tests:
Currently only one path if fully covered (similarity as it touches the most things)


