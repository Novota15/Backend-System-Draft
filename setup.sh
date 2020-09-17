#!/bin/bash

dnf -y update

dnf -y install epel-release

# install db
dnf -y install sqlite

# install python and pip
dnf -y install python3 python3-pip

# install python dependencies
pip3 install -r requirements.txt

# not sure why this won't install from the requirements file
pip3 install sqlalchemy

# build db
python3 db.py build_db

# add some URLs to the db
python3 db.py add_url https://naif.jpl.nasa.gov/pub/naif/generic_kernels/pck/gm_de431.tpc 1h
python3 db.py add_url https://naif.jpl.nasa.gov/pub/naif/generic_kernels/pck/earth_fixed.tf 2h

# make directory for storing files
mkdir file_storage

# install cron to create hourly cronjob
dnf -y install crontabs

# docker doesn't support systemd, we would need podman for this
# start cron daemon
# systemctl start crond.service

# enable cron on startup
# systemctl enable crond.service

#cp fetch-cron /etc/cron.d/fetch-cron

# give execution rights on cron job
chmod 0644 /etc/cron.d/fetch-cron

# apply hourly cron job for file fetching
crontab /etc/cron.d/fetch-cron

echo "setup complete"