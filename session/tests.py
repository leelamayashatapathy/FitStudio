from rest_framework.test import APITestCase
from rest_framework import status
import datetime
from session.models import Session, TimeSlot 


class SimpleFlowTests(APITestCase):
    def test_instructor_register_create_session_and_client_book(self):

        instructor_data = {
            "email": "inst1@example.com",
            "name": "Instructor One",
            "phone": "1234567890",
            "role": "instructor",
            "password": "StrongPass123!",
            "password2": "StrongPass123!"
        }
        reg_resp = self.client.post("/api/user/registration/", instructor_data, format='json')
        self.assertEqual(reg_resp.status_code, status.HTTP_201_CREATED)

        client_data = {
            "email": "client1@example.com",
            "name": "Client One",
            "phone": "0987654321",
            "role": "client",
            "password": "ClientPass123!",
            "password2": "ClientPass123!"
        }
        reg_resp_client = self.client.post("/api/user/registration/", client_data, format='json')
        self.assertEqual(reg_resp_client.status_code, status.HTTP_201_CREATED)

        login_resp = self.client.post("/api/login/", {
            "email": instructor_data["email"],
            "password": instructor_data["password"]
        }, format='json')
        self.assertEqual(login_resp.status_code, status.HTTP_200_OK)
        instructor_token = login_resp.data['token']['access']
        instructor_auth = {'HTTP_AUTHORIZATION': f'Bearer {instructor_token}'}

        session_data = {
            "title": "Morning Yoga",
            "category": "Yoga",
            "description": "Relaxing session",
            "date": "2025-06-04",
            "time_slots": [
                {"start_time": "09:00 AM", "end_time": "10:00 AM", "capacity": 5}
            ]
        }
        create_resp = self.client.post("/api/sessions/create/", session_data, format='json', **instructor_auth)
        print(create_resp.data)
        self.assertEqual(create_resp.status_code, status.HTTP_201_CREATED)

        session_data = create_resp.data['data']
        session_id = session_data['id']
        timeslot_id = session_data['time_slots'][0]['id']
        login_resp_client = self.client.post("/api/login/", {
            "email": client_data["email"],
            "password": client_data["password"]
        }, format='json')
        self.assertEqual(login_resp_client.status_code, status.HTTP_200_OK)
        client_token = login_resp_client.data['token']['access']
        client_auth = {'HTTP_AUTHORIZATION': f'Bearer {client_token}'}
        # print(client_auth)

        booking_url = "/api/client/book/session/"
        booking_resp = self.client.post(booking_url, {"timeslot": timeslot_id, "session": session_id}, format='json', **client_auth)
        # print("Booking response:", booking_resp.status_code, booking_resp.data)
        self.assertEqual(booking_resp.status_code, status.HTTP_201_CREATED)
