# Rock Scissors Paper API
JanKenGuu ;)

## Prerequisites
Docker
Python 3.9

## Build image and launch docker container
```
docker build -t jankenguu .
docker run --name jankenguu -p 8044:8044 jankenguu
```
You should be able to connect at : http://localhost:8044/



## Testing API
You can connect to : http://localhost:8044/docs

Or

Requests can be tested with the **request_test.http** file
with REST Client for Visual Studio Code
VS Marketplace Link: https://marketplace.visualstudio.com/items?itemName=humao.rest-client

## Launch pytest on docker container
```
docker exec -it jankenguu /bin/bash
pytest -vv
```

## Launch API server on local machine
directory jankenguu
uvicorn app.api:app --reload --port 8044

