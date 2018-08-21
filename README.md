# vCar

## vCar is a Driving Behaviour Analytics Platfom

vCar Driving Analytics Solution processes the data coming from the connected vehicle and generates advanced driving behavior
and driving pattern reports. The data is collected and analysed with the ultimate goal to gain a full understanding of
the drivers capability to adjust his driving based on driving conditions.

## Instalation

### build static files

Install dependencies :
`npm install`

* Production :

`gulp build --prod`
Then you need to set DEBUG=False in config/config.py

* Development :
  * `gulp build [--dev]` to generate static files.
  * `gulp watch` to watch static files.

### Install Elasticsearch

* Download at [Elasticsearch](https://www.elastic.co/products/elasticsearch)
* (Optionel) [Kibana](https://www.elastic.co/products/kibana)

### Install Redis

* Download at [Redis](https://redis.io/download)

### Docker integration :
To run vcar inside docker please make this changes:

Change `REDIS_HOST` and `ELASTICSEARCH_HOST` in `importer/platforms/openxc/constants.py` to : 

`REDIS_HOST = 'redis'`

`ELASTICSEARCH_HOST = 'elastic'`
then run :
`docker-compose up`

## Technologies

Python, FLASK, MYSQL, REDIS, ELASTIC, DOCKER, VISJS, NODEJS, BOOTSTRAP, CSS, JINJA2, HTML

## Platform Insights

* Car data storages
* Data visualization
* Driving Behavior

## Team members

boubouhkarim
SRamah
