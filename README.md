# Asynchronous Tasks with FastAPI and Celery

Example of how to handle background processes with FastAPI, Celery, and Docker.

## Want to learn how to build this?

Check out the [post](https://testdriven.io/blog/fastapi-and-celery/).

## Get it up and running

- **UI to trigger task:** http://localhost:8004/
- **Swagger UI to trigger task:** http://localhost:8004/docs
- **Task related CRUD:** http://localhost:8005/docs
- **Chart generator:** http://localhost:8006/docs
- **Flower to monitor task:** http://localhost:5556/
- **Promethesus:** http://localhost:9090/
- **Grafana:** http://localhost:3000/

![Alt Text](https://github.com/pandalearnstocode/fastapi-ms/blob/develop/endpoints.gif)

Username and password for grafana is `admin` and `admin`.

## Want to use this project?

Spin up the containers:

```sh
$ docker-compose up -d --build
```

Open your browser to [http://localhost:8004](http://localhost:8004) to view the app or to [http://localhost:5556](http://localhost:5556) to view the Flower dashboard.

Trigger a new task:

```sh
$ curl http://localhost:8004/tasks -H "Content-Type: application/json" --data '{"type": 0}'
```

Check the status:

```sh
$ curl http://localhost:8004/tasks/<TASK_ID>
```

### Charting data

![Alt Text](https://github.com/pandalearnstocode/fastapi-ms/blob/develop/generate_data.gif)
