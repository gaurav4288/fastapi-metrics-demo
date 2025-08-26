from fastapi import FastAPI
from prometheus_client import Counter, Histogram, generate_latest
from fastapi.responses import Response
import time
import random

app = FastAPI()

REQUEST_COUNT = Counter("request_count", "Total request count", ["method", "endpoint"])
REQUEST_LATENCY = Histogram("request_latency_seconds", "Request latency", ["endpoint"])

@app.get("/hello")
def hello():
    start = time.time()
    time.sleep(random.uniform(0.1, 0.5))  
    REQUEST_COUNT.labels(method="GET", endpoint="/hello").inc()
    REQUEST_LATENCY.labels(endpoint="/hello").observe(time.time() - start)
    return {"message": "Hello, world!"}

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type="text/plain")
