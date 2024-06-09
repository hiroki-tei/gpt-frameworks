# original repository
https://github.com/SciPhi-AI/R2R

# run quickly

## server

```
$ poetry run python -m r2r.examples.servers.configurable_pipeline
```

server will activate with following console output
```
INFO:     Started server process [45724]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

## client

In client/ directory, change client.sh like following with your file path.

```
client.sh

- FILE_PATH=/path/to/file.pdf
+ FILE_PATH=<your_file_path>
```

also, you can change user question in params/*.json

```
-  "message": "君の名は?",
+   "message": "<your_question>",
```


then, execute client.sh with subcommand like following.

```
sh client.sh <upload|search|rag_completion>

* upload: upload your file and turn them into vector.
* search: retrieve contexts with your question.
* rag_completion: generate answer with your question.
```

As you can see, file name under params/ directory (`search`, `rag_completion`) correspond to the subcommand of `client.sh`.
This means, ./client.sh search command uses `params/search.json` as request parameter and same as `rag_completion`.

