from locust import HttpUser, task, between

class HiveBoxUser(HttpUser):
    wait_time = between(1, 3)  # each simulated user waits 1-3s between requests

    @task(3)  # weight 3 — called 3x as often as store
    def get_temperature(self):
        self.client.get("/temperature")

    @task(1)
    def get_version(self):
        self.client.get("/version")

    @task(1)
    def store_data(self):
        self.client.get("/store")