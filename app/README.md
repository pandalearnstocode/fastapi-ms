## `app` folders directory structure

```bash
.
├── Dockerfile                      # docker file
├── logs                            # logs directory
│   └── celery.log                  # file where celery logs will be stores
├── main.py                         # fastapi entry pint
├── requirements.txt                # dependency file
├── static                          # All the UI assets
│   ├── main.css                    # Required CSS file for landing page
│   └── main.js                     # Required JS file for landing page
├── templates                       # HTML template folder for landing page
│   ├── _base.html                  # HTML page components
│   ├── footer.html                 # HTML page components
│   └── home.html                   # HTML page components
├── tests                           # Tests folder
│   ├── conftest.py                 # Test configuration
│   ├── __init__.py                 # __init__ file
│   └── test_tasks.py               # Unit test for defined routes
└── worker.py                       # Celery worker
```

## Reference link for the app

Ref: https://towardsdatascience.com/data-science-quick-tips-012-creating-a-machine-learning-inference-api-with-fastapi-bb6bcd0e6b01


### `prediction` sample payload


```json
{"sepal_length":5.1,"sepal_width":3.5,"petal_length":1.4,"petal_width":0.2}
```