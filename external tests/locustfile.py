from locust import HttpLocust, TaskSet, task

class UserBehavior(TaskSet):
    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """
        self.login()
        self.disclaimer()

    def login(self):
        response = self.client.get('/')
        csrftoken = response.cookies['csrftoken']
        self.client.post("/accounts/login/", {"username":"zo","password":"zo"},headers={'X-CSRFToken': csrftoken})
    
    def disclaimer(self):
        response = self.client.get('/disclaimer/')
        csrftoken = response.cookies['csrftoken']
        self.client.post("/disclaimer/", {},headers={'X-CSRFToken': csrftoken})

    @task(1)
    def heading(self):
        self.client.get("/symptom/information/1")

class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 0
    max_wait = 0