![microservices](microservices.png "Microservices communications ")


## Integration testing

The system has lot of integration tests where all services are teseted and the system is tested as a unit. The tests use a special test database so they don't share the database with the main system. 

**Running the tests**  
To run the test first a test server is started:
```console
 docker-compose -f docker-compose.test.yml build && docker-compose -f docker-compose.test.yml up
```
After the server is up and ready the tests can be run with:
```console
 docker-compose -f docker-compose.testrunner.yml  build && docker-compose -f docker-compose.testrunner.yml  up
```

Note: Before each test everything is deleted from the database and the database re-initialized.