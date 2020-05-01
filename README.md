# saturn
Python web application for automatic generation of video content from audio and image files

In order to run the application first install docker, then clone the repository and type the following within the top level directory in order to create the necessary docker image:
```console
$ docker build -t saturn_api
```

Then in order to spin up the web application on your local machine type:
```console
$ docker-compose up
```

Visit the following URL for the swagger documentation:
http://localhost:5004/api/v1/
