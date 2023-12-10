VPN service 
================
Vpn service with User`s loging and save data.<br>
Used Django framework.

## How to clone the repository?

To clone the repository, run the following command

```
git clone https://github.com/hito-de-jiro/vpn-service
```

## How to run it?

1. We are using shared folders to enable live code reloading. Without this, Docker Compose will not start:
    - Windows/MacOS: Add the cloned `vpn-service` directory to Docker shared directories (Preferences -> Resources -> File sharing).
    - Windows/MacOS: Make sure that in Docker preferences you have dedicated at least 5 GB of memory (Preferences -> Resources -> Advanced).
    - Linux: No action is required, sharing is already enabled and memory for the Docker engine is not limited.

2. Go to the cloned directory:
    ```shell
    cd vpn-service
    ```
3. Build the application:
    ```shell
    docker compose build
    ```
4. Make migrations ...
   ```shell
    docker compose run --rm web python manage.py makemigrations
    ```
5. ... and migrate.
   ```shell
    docker compose run --rm web python manage.py migrate
    ```
6. Populate the database with example data and create the admin user:
    ```shell
    docker compose run --rm web python manage.py createsuperuser
    ```
7. Run the application:
    ```shell
    docker compose up
    ```
8. Stop the application:
    ```shell
    docker compose stop
    ```
   
The service is available at the [link](http://127.0.0.1:8000/).

    
