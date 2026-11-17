# The Gatherer : Backend

This is a server application written in python.
It makes use of the FastAPI framework and utilizes Uvicorn to run it.

Static files as index.html are served from the dist directory of the [Frontend] project.
The API can be accessed as http(s)://[hostname]:[port]/api – the implementation resides in the **api** package.

[Frontend]: ../Frontend/README.md