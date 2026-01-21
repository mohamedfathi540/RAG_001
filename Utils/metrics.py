from prometheus_client import Counter, Histogram, generate_latest , CONTENT_TYPE_LATEST
from fastapi import Request, Response,FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
import time

#Define metrics

REQUEST_COUNT = Counter(
    'http_request_count',
    'Total HTTP request count',
    ['method', 'endpoint', 'status_code']
)

REQUEST_LATENCY = Histogram(
    'http_request_latency',
    'HTTP request latency',
    ['method', 'endpoint']
)

#

