import requests

class ApiService:
    def __init__(self):
        self.base_url = "http://localhost:5000"
        self.token = ""

    def get_token(self):
        return self.token

    def get_headers(self, auth=True, file=False):
        headers = {
            "Content-Type": "application/json",
        }

        if auth:
            headers["Authorization"] = "Bearer " + self.get_token()

        if file:
            headers["Content-Type"] = "multipart/form-data"

        return headers

    def get(self, endpoint, auth=True, params={}, is_blob=False):
        try:
            headers = self.get_headers(auth)
            response = requests.get(f"{self.base_url}/{endpoint}", headers=headers, params=params)

            if is_blob:
                return response.content
            
            if response.status_code == 401:
                print("Unauthorized")
                return None
            
            if response.status_code == 404:
                print("Not Found")
                return None
            
            if response.status_code == 500:
                print("Internal Server Error")
                return None
            
            if response.status_code == 400:
                print("Bad Request")

            return response.json()
        except:
            return None

    def post(self, endpoint, data=None, auth=True, files=False):
        try:
            headers = self.get_headers(auth, files)
            response = requests.post(f"{self.base_url}/{endpoint}", headers=headers, json=data)

            if response.status_code == 401:
                print("Unauthorized")
                return None
            
            if response.status_code == 404:
                print("Not Found")
                return None
            
            if response.status_code == 500:
                print("Internal Server Error")
                return None
            
            if response.status_code == 400:
                print("Bad Request")

            return response.json()
        except:
            return None

    def put(self, endpoint, data=None, auth=True):
        try:
            headers = self.get_headers(auth)
            response = requests.put(f"{self.base_url}/{endpoint}", headers=headers, json=data)

            if response.status_code == 401:
                print("Unauthorized")
                return None
            
            if response.status_code == 404:
                print("Not Found")
                return None
            
            if response.status_code == 500:
                print("Internal Server Error")
                return None
            
            if response.status_code == 400:
                print("Bad Request")

            return response.json()
        except:
            return None

    def delete(self, endpoint, auth=True, files=False):
        try:
            headers = self.get_headers(auth, files)
            response = requests.delete(f"{self.base_url}/{endpoint}", headers=headers)

            if response.status_code == 401:
                print("Unauthorized")
                return None
            
            if response.status_code == 404:
                print("Not Found")
                return None
            
            if response.status_code == 500:
                print("Internal Server Error")
                return None
            
            if response.status_code == 400:
                print("Bad Request")

            return response.json()
        except:
            return None
    


    # *** Auth ***
    def login(self, username=None, email=None, password=None):
        if username is None and email is None:
            raise ValueError("Either username or email must be provided")

        data = {"password": password}

        if username is not None:
            data["username"] = username
        else:
            data["email"] = email

        response = self.post("/login", data=data)

        return response
    
    def register(self, username, email, password, name, role, gender, birth_date):
        data = {
            "username": username,
            "email": email,
            "password": password,
            "name": name,
            "role": role,
            "gender": gender,
            "birth_date": birth_date
        }

        response = self.post("register", data=data)

        return response
    

    def verify_email_code(self, email, code):
        data = {
            "email": email,
            "code": code
        }

        response = self.post("verify-email-code", data=data)

        if 'token' in response:
            self.token = response['token']

        return response

    def resend_verification_code(self, email):
        data = {
            "email": email
        }

        response = self.post("resend-verification-code", data=data)

        if 'token' in response:
            self.token = response['token']

        return response


    # *** Users ***
    def get_me(self):
        response = self.get("users/me")
        return response

    def update_me(self, username, email, password, name, role, gender, birthdate, profile_picture, bio, links, private, vip, followers, body_measures, training_programs, following):
        data = {
            "username": username,
            "email": email,
            "password": password,
            "name": name,
            "role": role,
            "gender": gender,
            "birthdate": birthdate,
            "profile_picture": profile_picture,
            "bio": bio,
            "links": links,
            "private": private,
            "vip": vip,
            "followers": followers,
            "body_measures": body_measures,
            "training_programs": training_programs,
            "following": following
        }

        response = self.put("users/me", data=data)
        return response

    def delete_me(self):
        response = self.delete("users/me")
        return response

    def get_users(self):
        response = self.get("users/")
        return response

    def get_user(self, id):
        response = self.get(f"users/{id}")
        return response
    
    def get_admin_users(self):
        response = self.get("/admin/users/")
        return response

    def get_admin_user(self, id):
        response = self.get(f"/admin/users/{id}")
        return response

    def delete_admin_user(self, id):
        response = self.delete(f"/admin/users/{id}")
        return response
    

    # *** Training Programs ***
    def get_all_training_programs(self):
        response = self.get("/training-programs/")
        return response

    def get_one_training_program(self, id):
        response = self.get(f"/training-programs/{id}")
        return response

    def create_training_program(self, name, description, exercises):
        data = {
            "name": name,
            "description": description,
            "exercises": exercises
        }

        response = self.post("/training-programs/", data=data)
        return response

    def update_training_program(self, id, name, description, avg_duration, avg_volume, avg_reps, avg_sets, exercises):
        data = {
            "name": name,
            "description": description,
            "avg_duration": avg_duration,
            "avg_volume": avg_volume,
            "avg_reps": avg_reps,
            "avg_sets": avg_sets,
            "exercises": exercises
        }

        response = self.put(f"/training-programs/{id}", data=data)
        return response

    def delete_training_program(self, id):
        response = self.delete(f"/training-programs/{id}")
        return response
    

    # *** Trainings ***
    def get_all_trainings(self, training_program_id):
        response = self.get(f"/training-programs/{training_program_id}/trainings/")
        return response

    def get_one_training(self, training_program_id, id):
        response = self.get(f"/training-programs/{training_program_id}/trainings/{id}")
        return response

    def create_training(self, training_program_id, date, duration, volume, reps, sets, exercises, image, description, visibility):
        data = {
            "date": date,
            "duration": duration,
            "volume": volume,
            "reps": reps,
            "sets": sets,
            "exercises": exercises,
            "image": image,
            "description": description,
            "visibility": visibility
        }

        response = self.post(f"/training-programs/{training_program_id}/trainings/", data=data)
        return response

    def update_training(self, training_program_id, id, date, duration, volume, reps, sets, exercises, image, description, visibility):
        data = {
            "date": date,
            "duration": duration,
            "volume": volume,
            "reps": reps,
            "sets": sets,
            "exercises": exercises,
            "image": image,
            "description": description,
            "visibility": visibility
        }

        response = self.put(f"/training-programs/{training_program_id}/trainings/{id}", data=data)
        return response

    def delete_training(self, training_program_id, id):
        response = self.delete(f"/training-programs/{training_program_id}/trainings/{id}")
        return response
    

    # *** Exercises ***
    def get_all_exercises(self, muscle=None):
        params = {}
        if muscle is not None:
            params['muscle'] = muscle
        response = self.get("/exercises/", params=params)
        return response

    def get_one_exercise(self, id):
        response = self.get(f"/exercises/{id}")
        return response

    def create_exercise(self, name, muscle, description=None, category=None, equipment=None, secondary_muscle=None, video=None, image=None):
        data = {
            "name": name,
            "muscle": muscle,
            "description": description,
            "category": category,
            "equipment": equipment,
            "secondary_muscle": secondary_muscle,
            "video": video,
            "image": image
        }

        response = self.post("/exercises/", data=data)
        return response

    def update_exercise(self, id, name, muscle, description=None, category=None, equipment=None, secondary_muscle=None, video=None, image=None):
        data = {
            "name": name,
            "muscle": muscle,
            "description": description,
            "category": category,
            "equipment": equipment,
            "secondary_muscle": secondary_muscle,
            "video": video,
            "image": image
        }

        response = self.put(f"/exercises/{id}", data=data)
        return response

    def delete_exercise(self, id):
        response = self.delete(f"/exercises/{id}")
        return response
    

    # *** Posts ***
    def get_all_posts(self):
        response = self.get("/posts/")
        return response

    def get_one_post(self, id):
        response = self.get(f"/posts/{id}")
        return response

    def create_post(self, title, content, training_id):
        data = {
            "title": title,
            "content": content,
            "training_id": training_id
        }

        response = self.post("/posts/", data=data)
        return response

    def update_post(self, id, title, content, training_id, likes, comments):
        data = {
            "title": title,
            "content": content,
            "training_id": training_id,
            "likes": likes,
            "comments": comments
        }

        response = self.put(f"/posts/{id}", data=data)
        return response

    def delete_post(self, id):
        response = self.delete(f"/posts/{id}")
        return response

    



