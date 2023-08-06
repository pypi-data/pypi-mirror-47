# Server setup

# Worker setup

env variables used to setup mq connection parameters<br>
RABBITMQ_HOST=<br>
RABBITMQ_USER=<br>
RABBITMQ_PASS=<br>



# Releases
## Docker 
###Base repository<br>
<b>registry.gitlab.com/aicu/lab/aicu_micropipes</b><br>
###Latest version<br>
<b>registry.gitlab.com/aicu/lab/aicu_micropipes:latest</b><br>
###Tagged version<br>
registry.gitlab.com/aicu/lab/aicu_micropipes:0.0.1<br>
registry.gitlab.com/aicu/lab/aicu_micropipes:0.0.2<br>
...<br>

## Helm chart


## Python package
versioning as other tags<br> 
<b>pip install micropipes-worker</b>

https://pypi.org/project/micropipes-worker/

# Another comments


env variable used to setup log level
LOG_LEVEL=INFO

# Job status explanation
## 'status.wait' 
processing paused, save status, keep resources, job will continue
## 'status.started' 
start processing
## 'status.finished' 
processing finished correctly, free resources, job will not continue
## 'status.canceled' 
processing finished unexpectedly, free resources, job will not continue
##  'status.stop' 
processing paused, save status, free resources, job will continue