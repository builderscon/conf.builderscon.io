# builderscon.io

This application implements the https://builderscon.io site.

Features include:

* Handles multiple conference series (i.e. Conference "X" 2016, 2017, 2018... and Conference "Y" 2016, 2017, 2018... etc)
* Internationalized (currently supports Japanese and English)
* Github/Twitter/Facebook login
* Capability to track user proposal submissions over time (so you know which proposals were sent to which conference)
* Capability to display sessions for a given user over time (so you can view all of their video/slides)
* Custom redirects for conferences that do not want to use our site, but want to register their data through [octav](https://github.com/builderscon/octav)
* Automatic session timetable generation
* Automatic conference staff page generation
* Customizable session submission workflow

## How to run on Vagrant

1.  setup

    ```
    $ vagrant up
    ```


2.  configure, edit config.json

    Currently OCTAB section is empty.
    Please set proper values to run correctly.

3.  start server in simple server.

    ```
    $ vagrant ssh
    $ cd ~/vagrant
    $ redis-server &
    $ gunicorn app:app
    ```

4.  access <http://127.0.0.1:3000/>

## How to run on GAE local dev server (work in progress, as we did not fully migrate to GAE yet)

1.  setup GAE SDK

  - Install [GAE Python SDK](https://cloud.google.com/appengine/downloads)   

2.  start GAE local dev server
  
    do not forget the last dot (.) in the command

    ```
    $ dev_appserver.py .
    ```

4.  access <http://127.0.0.1:8080/>


## i18n/l10n

### Extract translatable strings from templates

```
pybabel extract --mapping babel.cfg --output messages.pot .
```

### Initialize message catalogs (ONLY DO THIS ONCE for $locale)

```
pybabel init --input-file messages.pot --output-dir translations/ --domain messages --locale $locale 
```

### Update message catalogs when messages.pot changes

```
pybabel update --input-file messages.pot --output-dir translations/ --domain messages --locale $locale 
```

### Compile message catalogs

```
pybabel compile --directory translations/ --domain messages
```
