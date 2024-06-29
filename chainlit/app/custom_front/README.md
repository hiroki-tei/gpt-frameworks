# backend

`./back` directory is the main directory for python server app as backend

## prerequisite

### environment variables

you need to put `CHAINLIT_AUTH_SECRET` in `./back/.env` file.
just hitting `poetry run chainlit create-secret` will create random one for you in stdout.

## start server
(in `./back` dir)

`poetry run uvicorn app:app --host 0.0.0.0 --port 80`

# frontend

`./front` directory is the main directory for react app as frontend

## prerequisite

### package manager 

please use yarn v1.22.22.
Other manager might able to use but is not tested at all.

### install npm modules
(in `./front` dir)

`yarn install`


## start front app

`yarn run dev`



`