# fRAGme 
### This is a dockerized RAG FastAPI service with vector store handling.

## Setup
### Start FastAPI webservice
```shell
$ git clone git@github.com:krauhen/fRAGme.git
$ cd fRAGme
$ python -m venv venv
$ source venv/bin/activate
(venv)$ pip install .
(venv)$ export OPENAI_API_KEY="YOUR_OPENAI_API_KEY"
(venv)$ uvicorn src.fRAGme.app:app --host 0.0.0.0 --port 8080
```

### Start docker
```shell
$ git clone git@github.com:krauhen/fRAGme.git
$ cd fRAGme
```
Replace OPENAI_API_KEY in ".env" file with your OpenAI API-Key.
```shell
(venv)$ docker-compose build
(venv)$ docker-compose up
```
#### Environment variables (see .env)
| Variable       | Default Value |
|----------------|---------------|
| PORT           | 8080          |
| HOST           | 0.0.0.0       |
| PROXY_PATH     | empty         |
| ORIGIN         | *             |
| OPENAI_API_KEY | empty         |
| DATA_PATH      | ./data        |
