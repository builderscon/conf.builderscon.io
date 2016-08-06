# builderscon.io

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
    $ python app.py
    ```

4.  access <http://127.0.0.1:3000/>

## How to run on GAE local dev server (work in progress, as we did not migrate to GAE yet)

GAE doesn't support Redis. So you need to use Memcache instead.

1.  setup

  - Install [GAE Python SDK](https://cloud.google.com/appengine/downloads)
    

2.  In config.json,

   Remove the "REDIS_INFO" section :
   
   ```
       "REDIS_INFO": {
         ...
       },
   ```

   and add the "MEMCACHE" section like below

   ```
    "MEMCACHE": {
        "servers" : [
            {
                "host": "localhost",
                "port": "11211"
            }
        ],
        "debug": 0
    },  
   ```

3.  start GAE local dev server
  
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
pybabel init --input-file messages.pot --output-dir translations/ --locale $locale --domain messages
```

### Update message catalogs when messages.pot changes

```
pybabel update --input-file messages.pot --output-dir translations/ --locale $locale --domain messages
```

### Compile message catalogs

```
pybabel compile --directory translations/ --domain messages
```
