# URL Shortener
## Requirements
 - Python3
 - Docker/Docker compose

## How to build/run the project
 - In the projec root folder run:`docker compose build`
 - Run: `docker-compose up`

## Endpoints
This project uses FastAPI, so, once the project is running, go to: `localhost/docs`
There you'll find 4 endpoints:
 - `/` Read root [GET] Used for testing that everything's up
 - `/url` Create url [POST]
 - `/{url_key}` Forward to target Url [GET] - In this endpoint you can
 use the key generated from `/url` [POST] endpoint to go to the page you wanted, so, let's say that you have the code `FEDAX`, in your browser you'd hit: `localhost/FEDAX` and it will get you to the original url you targeted
 - `geturlfromkey/{url_key}` get url from key [GET] - Right here you get the complete json body


## How to run the tests
 - With the project running, execute: `docker exec -it api pytest -s`