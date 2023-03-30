from django.test import TestCase
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from projects.models import *
from django.urls import reverse


class Tests(APITestCase) :
    def test_member(self):
        response = self.client.get('/api/project/1/members',format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        if ( response.status_code == 200):
            print("   API - GET endpoint for members --------- OK")

    def test_suggestion(self):
        response = self.client.get('/api/project/1/suggestions',format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        if ( response.status_code == 200):
            print("  API - GET endpoint for suggestions --------- OK")

    def test_tasks(self):
        response = self.client.get('/api/projects/1/tasks',format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        if ( response.status_code == 200):
            print("  API - GET endpoint for tasks --------- OK")

    def test_riskevaluation(self):
        response = self.client.get('/api/projects/1/riskevaluation',format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        if ( response.status_code == 200):
            print("  API - GET endpoint for risk evaluation --------- OK")

    def test_meetings(self):
        response = self.client.get('/api/projects/1/meetings',format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        if ( response.status_code == 200):
            print("  API - GET endpoint for meetings --------- OK")


    def test_feedback(self):
        response = self.client.get('/api/projects/1/feedback',format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        if ( response.status_code == 200):
            print("  API - GET endpoint for feedback --------- OK")

    def test_userprofile(self):
        response = self.client.get('/api/users/1/myaccount',format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        if ( response.status_code == 200):
            print("  API - GET endpoint for user profile --------- OK")


    def test_userskills(self):
        response = self.client.get('/api/users/1/skills',format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        if ( response.status_code == 200):
            print("  API - GET endpoint for user skills --------- OK")
    
    def test_generatingsuggestion(self):
        response = self.client.get('/api/projects/1/suggestion',format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        if ( response.status_code == 200):
            print("  API - GET endpoint for generating suggestions--------- OK")
    
    def test_generating_risk_evaluation(self):
        response = self.client.get('/api/projects/1/riskevaluation',format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        if ( response.status_code == 200):
            print("  API - GET endpoint for generating risk evaluation--------- OK")

    def test_role_requirement(self):
        response = self.client.get('/api/role/rolerequirement',format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        if ( response.status_code == 200):
            print("  API - GET endpoint for role requirements --------- OK")

    def test_create_user(self):
        client = APIClient()
        client.login(username="admin",password="admin")

        test = User.objects.create(username = 'John', password = '12345' , email = "example@gmail.com")

        response = self.client.get('/api/users/', test, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        if ( response.status_code == 200):
            print("  API - POST endpoint for user --------- OK")

    def test_update_user(self):
        client = APIClient()
        client.login(username="admin",password="admin")

        info = { 
            "username" = 'Doe',
        }

        response = self.client.put('/api/users/1',info,format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        if ( response.status_code == 200):
            print("  API - PUT endpoint for user --------- OK")

    def test_skill(self):
        response = self.client.get('/api/skills/',format='json')
        print("  API - GET endpoint for skills --------- OK")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_role(self):
        response = self.client.get('/api/roles/',format='json')
        print("  API - GET endpoint for roles --------- OK")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_project(self):
        #Login user for authorization and authentication purposes
        client = APIClient()
        client.login(username="admin",password="admin")

        response = client.get('/api/projects/',format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        if ( response.status_code == 200):
            print("  API - GET endpoint for projects --------- OK")

    def test_create(self):
        #Login user for authorization and authentication purposes
        client = APIClient()
        client.login(username='admin',password='admin')

        test_post = Project.objects.create(
            name = 'Test Project',
            description = 'Test Create',
            methodology = 'Agile',
            client_name = 'DB'
        )

        response = client.create('/api/projects/',format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        if ( response.status_code == 200):
            print("  API - POST endpoint for projects --------- OK")
    
    def test_update(self):
        #Login user for authorization and authentication purposes
        client = APIClient()
        client.login(username='admin',password='admin')

        response = client.put('/api/skills/3', {
            "name" : "Test Update",
            "description" : "Test Update"
        }, format = 'json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        if ( response.status_code == 200):
            print("  API - PUT endpoint for projects --------- OK")

    def test_task(self):
        #Login user for authorization and authentication purposes
        client = APIClient()
        client.login(username='admin',password='admin')

        response = client.get('/api/projects/1/task',format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        if ( response.status_code == 200):
            print("  API - GET endpoint for projects --------- OK")

    def test_create(self):
        #Login user for authorization and authentication purposes
        client = APIClient()
        client.login(username='admin',password='admin')

        test_post = Skill.objects.create(
            name = 'Test Create',
            description = 'Test Create'
        )

        response = client.post('/api/users/', test_post, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        if ( response.status_code == 200):
            print("   API - POST endpoint for tasks --------- OK")
    
    def test_delete(self):
        #Login user for authorization and authentication purposes
        client = APIClient()
        client.login(username='admin',password='admin')
        response = client.delete('/api/skills/3',format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        if ( response.status_code == 200):
            print("  API - DELETE endpoint for tasks --------- OK")

