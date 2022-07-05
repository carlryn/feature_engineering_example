# Feature engineering tasks

This is a simple project showing a simple feature engineering pipeline!

###  How to run
Recommended requirements:
* docker
* docker-compose
* Folder called output where the program outputs the csv files. You could of course also just port into the docker container and read the files from there if you don't want to bind any volumes.


````
docker-compose build
docker-compose up
docker-compose run --entrypoint "" feature-engineering-example python -m pytest # For running tests
````

Docker compose reads env variables from the .env which then is translated into arguments in the program. Change the env variables => the output will be effected.

If you are running on a windows machine you might run into some issues with the binding of the output volume. Then consider porting into the container instead.

The dockerfile for this project I use in most of my projects. By extending differrent base images I can very easily incorporate GPU support, or java(spark). Large parts of it can also be uploaded to a docker repo to make builds go faster.
