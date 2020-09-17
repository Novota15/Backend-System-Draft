FROM centos:8
ENV container docker
LABEL maintainer "Grant"

# move app files into the container
ADD setup.sh /setup.sh
ADD db.py /db.py
ADD fetch.py /fetch.py
ADD requirements.txt /requirements.txt
ADD fetch-cron /etc/cron.d/fetch-cron

# give executable permission on setup script
RUN chmod u+x /setup.sh
RUN /setup.sh

# need to run cron, can't use systemd in docker
# the -n is to run the cronjob in the foreground so the container doesn't exit
CMD ["crond", "-n"]