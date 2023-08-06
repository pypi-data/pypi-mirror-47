# Lazo Index Service Client

Client library for indexing and querying the [Lazo Index Service](https://gitlab.com/ViDA-NYU/datamart/lazo-index-service).

## How to install?

    $ pip install lazo-index-service

## How to run?

First, instantiate the client:

```python
import lazo_index_service

lazo_client = lazo_index_service.LazoIndexClient(host=SERVER_HOST, port=SERVER_PORT)
```

where `SERVER_HOST` and `SERVER_PORT` are the hostname and the port where the Lazo index server is running, respectively.

To index a set of values:

```python
(n_permutations, hash_values, cardinality) = lazo_client.index_data(
    VALUES,
    DATASET_NAME,
    COLUMN_NAME
)
```

where `VALUES` is the list of string values, and `DATASET_NAME` and `COLUMN_NAME` are the names of the dataset/column from where the values come from.

To query the index:

```python
query_results = lazo_client.query_data(
    QUERY_VALUES
)
```

where `QUERY_VALUES` is the list of values to be used for the query.