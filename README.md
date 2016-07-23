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
