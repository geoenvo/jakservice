# README #

How to deploy JakSAFE webapp on Ubuntu 14.04.

### install requirements and create virtualenv ###

* sudo apt-get update
* sudo apt-get -y install build-essential python-pip python-dev python-software-properties git-core vim screen
* sudo pip install virtualenv virtualenvwrapper
* nano ~/.bashrc
    * \# add to end
    * export WORKON_HOME=$HOME/.virtualenvs
    * source /usr/local/bin/virtualenvwrapper.sh
* . .bashrc

### install mysql ###

* sudo apt-get -y install mysql-server libmysqlclient-dev
    * \# set root password
* mysql -u root -p
    * create database jaksafe;
    * grant all privileges on jaksafe.* to 'jaksafe'@'localhost' identified by 'password';
    * set password for 'jaksafe'@'localhost' = PASSWORD('password');
    * flush privileges;
    * exit;

### create virtualenv and track repo ###

* mkvirtualenv jaksafe
* cdvirtualenv
* git init
* git remote add origin git@bitbucket.org:irisiko/jaksafe.git
* git fetch
* git checkout -t origin/master

### install python packages in virtualenv ###

* pip install -r requirements.txt

### sync database ###

* cd jaksafe
* cp jaksafe/settings.py.sample jaksafe/settings.py
* nano jaksafe/settings.py
    * \# adjust database connection settings
    * \# check jakservice dirs
    * \# check PYTHON_EXEC path (use virtualenv python binary, or system one)
* python manage.py migrate
* python manage.py createsuperuser
    * \#enter admin account

### run jakSAFE sql script to create tables ###

* cdvirtualenv
* mysql -u jaksafe -p jaksafe < ./jaksafe_devfiles/jaksafe.sql

### prepare jakservice  ###

* cdvirtualenv
* cd jaksafe/jaksafe/jaksafe
* git clone git@bitbucket.org:irisiko/jakservice.git
* \# follow jakservice README.md

### run dev server ###

* python manage.py runserver 0.0.0.0:8000 \# open in browser http://SERVER_IP:8000
* OR
* start with supervisord: sudo ./start_supervisord.sh \# open in browser http://SERVER_IP