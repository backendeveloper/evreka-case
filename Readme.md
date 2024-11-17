## Target Case #1
You should be able to get location, speed, etc. location information intensively to Rest API
services (you can think of 1 million of this data per day). You can store this data in a
database of your choice. The data coming to API services should be processed
asynchronously, so you need to use a queue management tool, we currently use RabbitMQ
or Celery. We should be able to access this data for a specific date range + you should create
Rest API services where we can only access the last data for a device.

## Target Case #2
You should be able to receive data containing location, speed etc. location information over
TCP protocol (you can imagine 1 million of these data coming in a day). You can store this
data in a database of your choice. The location data coming from the devices to the TCP
server should be processed asynchronously because the open time of the connection
negatively affects the battery life of the devices sending data. We are currently using
RabbitMQ or Celery. You should prepare Rest API services where we can access the data
coming to the TCP server for a certain date range + the last data for only one device.


docker build -t analytics-api:latest ./../analytics-api     
docker build -t worker-api:latest ./../worker-api     
docker build -t gateway-api:latest ./../gateway-api 