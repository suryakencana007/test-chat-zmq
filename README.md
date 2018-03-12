# TEST API Chat menggunakan ZMQ

### Setup 

```python

    python3 -m venv env

    source env/bin/activate

    pip install -r requirements.txt

```

### Running API

```python
    
    # Menjalakan Worker Push-Pull 
    python worker.py

    # Menjalakan API App
    python AppSanic.py

```

## API Doc

API Send Pesan
==============

```
  curl -i http://localhost:9090/push\?message\=hello-zmq

```


API Receiver Pesan
==============

```
  curl -i http://localhost:9090/stream

```
