from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from testapp.models import UserData
from rest_framework_simplejwt.tokens import RefreshToken
import json

class UserDataTestCase(TestCase):
    def setUp(self):

        self.user = User.objects.create_user(username="testuser", password="Test@password")
        self.client = APIClient()
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)

    def test_query_my_data(self):

        UserData.objects.create(user=self.user, title="Test Title 1", description="Description 1")
        UserData.objects.create(user=self.user, title="Test Title 2", description="Description 2")

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")

        query = """
        query {
            myData {
                id
                title
                description
            }
        }
        """
        response = self.client.post("/graphql/", {"query": query}, format="json")

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content.decode())["data"]["myData"]
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]["title"], "Test Title 1")
        self.assertEqual(data[1]["title"], "Test Title 2")

    def test_add_data_mutation(self):

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")

        mutation = """
        mutation {
            addData(title: "New Data", description: "This is a test") {
                id
                title
                description
            }
        }
        """
        response = self.client.post("/graphql/", {"query": mutation}, format="json")

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content.decode())["data"]["addData"]
        self.assertEqual(data["title"], "New Data")
        self.assertEqual(data["description"], "This is a test")

        user_data = UserData.objects.get(title="New Data")
        self.assertEqual(user_data.description, "This is a test")
        self.assertEqual(user_data.user.username, "testuser")

    # def test_unauthenticated_access(self):

    #     query = """
    #     query {
    #         myData {
    #             id
    #             title
    #             description
    #         }
    #     }
    #     """
    #     response = self.client.post("/graphql/", {"query": query}, format="json")

    #     self.assertEqual(response.status_code, 200)
    #     self.assertIn("Authentication required", str(response.json()["errors"]))
