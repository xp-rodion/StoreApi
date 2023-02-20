# Interview Rishat

## Setup

1. Clone repository

```shell
$ git clone https://github.com/xp-rodion/StoreApi.git
```

2. Configure environment:
    1. Copy example environment preset and open its:
    ```console
    $ cp .env.example .env && vim .env
    ```
    2. Configurate DB connection for local db or use default values for docker running(default already in env.example):
   ```text
   POSTGRES_USER=
   POSTGRES_PASSWORD=
   POSTGRES_HOST=
   POSTGRES_PORT=
   POSTGRES_DB=
   ```
   
   I will write the keys for stripe and django here:
   3. 
   ```text
      SECRET_KEY=django-insecure-j+&f=#oewr%mh)r5c%p^*0nd695agi-_g4-k!$$)$r4bq$w_(j
      STRIPE_PUB_KEY=pk_test_51MUuvEJE4wc8vNIdQq2Da8zV04wmR3Wk5NAQiAAqen0oVbSr2vp7zlhHeeZg0Y9WmlWB5ZtvElNO2tCitjNjc36600NMHC2Soj
      STRIPE_SEC_KEY=sk_test_51MUuvEJE4wc8vNIdaD2yATDtrrZQGI7MsJNYVbUjayN6UeJOAGpdvKs8QMNAnleBclCwVe4lMZUehPJU7g9SLXYz00WnAn6JdS
   ```
   4. 
      Default set for server:
    ```text
        SERVER_HOST=0.0.0.0
        SERVER_PORT=8000
      ```
3. Run server:
   1. 
      Inside container:
      ```console
      $ docker-compose up -d --build
      ```
   2. Using the admin panel, you can set up models and test the api or upload fixture data:
      ```console
      $ sudo docker exec -it web python manage.py loaddata --format=json [Model] > [JSON fixture].json
      ```
   