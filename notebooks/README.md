# Life cycle of DE, ML pipeline & model serving

## `job_template.ipynb`

* `DE pipeline`: from source DE pipeline will read the data. will validate, run ETL and validate file before uploading.
* `ML pipline`: after the data is refreshed in db, trigger pipeline, store output in DB.
* `ML serving`: when a user execute workload in it should, it should read model result from db and run workload.

[![Explanting the life cycle](https://img.youtube.com/vi/Oiclxv4S1P8/0.jpg)](https://www.youtube.com/watch?v=Oiclxv4S1P8)
