# File Fetching App Backend Architecture Draft 

## Components
* Fetching app - fetch.py
* Database app - db.py
* Package requirements file - requirements.txt
* Cronjob file - fetch-cron
* Docker file - Dockerfile
* Setup script - setup.sh

## Setup

run ```docker build .```

find container id with ```docker images -a```

start the container with ```docker run --name NAME ID#```

login to the interactive shell of the container ```docker exec -it NAME/ID bash```

The container uses an hourly cronjob that runs ***fetch.py*** outputs to the docker stderr and stdout.

### To check if the job is scheduled
```docker exec -ti <your-container-id> bash -c "crontab -l"```

### To check if the cron service is running
```docker exec -ti <your-container-id> bash -c "pgrep cron"```

stop the container with ```docker stop NAME/ID```

## Database Functions
* Build database: ```$ python3 db.py build_db```
* Print all database items ```$ python3 db.py dump```
* Add url to fetch: ```$ python3 db.py add_url ADDRESS INTERVAL``` - supports whole number invervals in hours or days (1h) or (1d)
* Modify url fetch interval ```$ python3 db.py set_interval ADDRESS INTERVAL```
* Enable/Disable url ```$ python3 db.py url_enabled ADDRESS True/False```