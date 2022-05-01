# technical-task
- - -
Simple application for storing users
- - -
### Api endpoints
* '/user/' :
  * GET - get all users
  * POST - create new user
* '/user/\<int:id>/' :
  * GET - get certain user by id
  * PUT - update certain user by id
  * PATCH - update some fields of a specific user 
  * DELETE - delete certain user by id
- - -
### Run application with docker
1.) First you need to run the database with the command : 

> docker-compose up mysql

2.) After that run the tests with the commad :

> docker-compose up webserver.test

3.) And in order to start the server, you need to use the following command :

> docker-compose up webserver

- - -
You can check the endpoints through **_Postman_**
- - -