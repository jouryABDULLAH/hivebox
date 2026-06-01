from prometheus_client import Counter, Gauge, Histogram 

sensebox_fetch_total = Counter(
    'sensebox_fetch_total',
    'Total senseBox API fetches',
    ['box_id', 'status']
)

sensebox_fetch_failures = Counter(
    'sensebox_fetch_failures_total',
    'Total failed senseBox API fetches',
    ['box_id']
)

cache_operations = Counter(
    'cache_operations_total',
    'Total cache operations',
    ['operation', 'status']  # operation: get/set, status: hit/miss/error
)


storage_operations = Counter(
    'storage_operations_total',
    'Total storage operations',
    ['status']  # success/failure
)

current_temperature = Gauge(
    'current_temperature_celsius',
    'Current average temperature from all boxes'
)


accessible_boxes = Gauge(
    'accessible_boxes_count',
    'Number of currently accessible senseBoxes'
)


sensebox_response_time = Histogram(
    'sensebox_response_time_seconds',
    'senseBox API response time',
    ['box_id'],
    buckets=[0.1, 0.5, 1.0, 2.0, 5.0, 10.0]  # Response time buckets
)

temperature_fetch_duration = Histogram(
    'temperature_fetch_duration_seconds',
    'Time to fetch and process all temperature data',
    buckets=[0.5, 1.0, 2.0, 5.0, 10.0]
)
