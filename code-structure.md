# Structure of code

## Init and running the app

### src

 * config.py: it creates that connexion using connexion framework.   It is based on connexion framework that generates the routes based on OpenAPISpecification YAML (in this case with swagger)
 * app.py: it takes the connexion with the config and applies the swagger yaml with all the routes. It also calls to the initializer.
 * swagger.yaml it contains all the routes and REST methods, and link each route with a controller method:
 ```
paths:
  /readings/store:
    post:
      operationId: controller.electricity_reading_controller.store
...
...
  /readings/read/{smart_meter_id}:
    get:
      operationId: controller.electricity_reading_controller.read
 ```
 * app_initializer.py: it just populate the "database" with
    * PricePlans: stored statically, so there is no service. It is just a repository 
        * Names and descriptions of plans
        * plans are stored as an array of objects of type PricePlan (./src/repository/price_plan_repository)
    * ElectricityReading: 
        * It users a controller (src/controller/electricity_reading_controler), that uses a service (src/services/electricity_reading_service) that prepares the data to be stored into a repository (src/repository/electric_reading_repository)
        * Store the list of smartmeters with its readings. With randome generator of X smartmeters and Y readings for each one.
        * There are no smartmeters list, there is a list of readings pointing to smartmeters
        * Each reading contains a timestamp (random) with a reading (random)
* domains/*  just the models
    * price_plan
    * electricity_reading
* controlers/*  with manages the models for the different operations. 
    * electrictity_reading_controller
    * price_plan_comparator_controller
* service/* which are the exposed services and connect to the repository to store/retrieve data
    * account_service
    * electricity_reading_service
    * price_plan_service
    * time_converter (not exposed through REST)
* repository/* which manages the data persistence
    * price_plan_repository
    * electricity_reading_repository


## Controllers to manage the different operations from the REST API

### src/controller/electricity_reading_controller

Store/read methods. It should contain the CRUD of each resource, but the problem is that this project is too service/functions oriented and not so resources oriented.

It just creates the service to do the store/read. 

Some examples of bad practices about RESTful APIs:

To get readings from a smartmeter:
```
  /readings/read/{smart_meter_id}:
    get:
      operationId: controller.electricity_reading_controller.read
```
It should be something like: GET  /smartmeters/{id}/readings
You should not use verbs on the urls definitions, like /.../READ/... 

Other example to compare plans:

```
 /price-plans/compare-all/{smart_meter_id}:
```

Instead it should be:

```
GET  /smartmeters/{id}/plan    -> for getting current plan
GET  /smartmeters/{id}/plan?compare=[plans]   -> for comparing plans
GET /plans/  -> for getting plans ids
```


## Services that interacts with the controller

### src/service/electric_reading_service

store/retrieve readings

It also connects with the repostiry to store the data

It receives readings/smartmeter as a json that is converter to the domain model ElectricityReading. Generating a list of ElectricityReadings:

```
ElectricityReading(time=997586118, reading=0.427) ElectricityReading(time=981058856, reading=0.43) ElectricityReading(time=999438027, reading=0.158) ElectricityReading(time=990526546, reading=0.031) ElectricityReading(time=979694410, reading=0.537)

``` 

This transformation is done by the service, which manages the type ElectricReading and uses the storage repository to just store in that way. Later new readings for this ide will be concatenated to the current ones.

The service calls to the repository with an extracted smartmeterid and the list of readings (no longer a json)


## Repositories that implements the persistance of the project

 In that case json in memory

### src/repository/electric_reading_repository

Repository implements methods store/find. In this case with a json on memory

It acts as a repostiroty or database. When storing, first retrieve the smartmeteid with the associated list of readings. It concatenates the new list of readings.

It is everything stored as a json on memory. In the way of:

{
 'smartmeter-0': [ List of objects type ElectricReading],
 'smartmeter-1': [ List of objects type ElectricReading]
}

Which is much more easily to manage about finding, storing and updating than the retrieved data:


  "smartMeterId": <smartMeterId>,
  "electricityReadings": [
    {
      "time": <timestamp>,
      "reading": <reading>
    }
  ]
}
Which is much more user-friendly, or much easier to generate data.


### src/repository/price_plan_repository

Repository implements methods store/get. In this case with a json on memory

Only a repository for price plans. It creates a class of type **PricePlan** (src/domain/price_plan). Which allows to store, and delete priceplan. A price plan contains just the prices


## Data generators

### src/generator/electricity_reading_generator

It just a couple of functions to make randome generators. Like the one that creates random electricity readings.


# General comments

 * Project too services oriented instead of resources oriented. This creates ugly urls, not very well browseable.
 * Controller should be more based on the same method for a CRUD over different resources
 * not all the tests done
