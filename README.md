# conf.builderscon.io

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
    $ python3 app.wsgi
    ```

4.  access <http://127.0.0.1:3000/>

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
