import random
from locust import HttpUser, task, between
from jose import jwt  

class SocialMediaUser(HttpUser):
    wait_time = between(1, 5)
    token = None
    my_user_id = None

    def on_start(self):
        """
        Logs in and dynamically captures the user ID from the token.
        """
        login_data = {
            "username": "hello124@gmail.com",
            "password": "password123"
        }
        
        
        response = self.client.post("/login", data=login_data)
        
        if response.status_code == 200:
            self.token = response.json().get("access_token")
            self.client.headers.update({"Authorization": f"Bearer {self.token}"})
            
            
            try:
                payload = jwt.get_unverified_claims(self.token)
                self.my_user_id = payload.get("user_id")
            except Exception as e:
                print(f"Could not decode token: {e}")
        else:
            print(f"Login failed: {response.status_code}")

    @task(4)
    def view_posts(self):
        
        self.client.get("/posts/")

    @task(2)
    def create_and_interact(self):
      
        new_post = {
            "title": f"Dynamic Load Test {random.randint(1, 1000)}",
            "content": "Testing with dynamic user IDs",
            "published": True
        }
        post_res = self.client.post("/posts/", json=new_post)
        
        if post_res.status_code == 201:
            post_id = post_res.json().get("id")
            self.client.post("/vote/", json={"post_id": post_id, "dir": 1})

    @task(1)
    def check_own_profile(self):
        
        if self.my_user_id:
            self.client.get(f"/users/{self.my_user_id}")