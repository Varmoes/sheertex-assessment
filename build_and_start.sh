#! /bin/sh
docker build -t coding-assessment-sheertex .

docker run -d -p 8080:8080 coding-assessment-sheertex