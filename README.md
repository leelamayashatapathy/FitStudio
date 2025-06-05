This is a Django REST API backend for managing sessions, time slots, and bookings for a fitness studio. Instructors can create sessions with time slots, and clients can book them. The system supports user role-based permissions, timezone-aware scheduling, and dynamic seat availability.


**Features**

Role-Based Access Control: Separate roles for instructors and clients with permission checks.

Session & TimeSlot Management: Instructors can create, update, and manage sessions and their associated time slots.

**Booking Management:**

Clients can book available slots only.

Automatically prevents bookings if the slot is full.

Enforces unique bookings (a client can’t book the same slot twice).

**Timezone**

Sessions and slots are created in IST (Indian Standard Time) by default.

All times are converted dynamically to the user’s timezone on retrieval.

Ensures accurate scheduling across different time zones.

**Error Handling:**

Returns clear, consistent error messages for invalid data and unauthorized actions.

Handles edge cases gracefully (e.g., trying to book expired or full slots).

**Detailed Session Views:**

Instructors can view their sessions with comprehensive booking details.

Public endpoints show available time slots and capacity status.

**Booking History:**

Clients can view their past and upcoming bookings.

**Capacity:** Time slots track how many seats are booked and available.

**API Security:** Protected endpoints using token authentication.

**Extensible Design:** Easy to add new features like notifications or filters.



**Run Project**

1. Clone the Repository
git clone https://github.com/your-username/fitness-studio.git

cd fitness-studio

2. Create a Virtual Environment & Activate It
python -m venv venv
**On Windows:**
venv\Scripts\activate
**On macOS/Linux:**
source venv/bin/activate

3. Install Dependencies
pip install -r requirements.txt

5. Apply Migrations
python manage.py makemigrations
python manage.py migrate

6. Create a Superuser
python manage.py createsuperuser

7. Run the Development Server
python manage.py runserver

Admin Panel: http://127.0.0.1:8000/admin/


**API's**

<!-- Authentication -->

POST: http://127.0.0.1:8000/api/login/ - Login with email and password

POST: http://127.0.0.1:8000/api/register/ - Register new user (with role: instructor or client)
-> Get the access token and paste it in Api's header Key: Authorization and value as: Bearer accesstoken 

POST: http://127.0.0.1:8000/api/refresh-token/ - Get new access token by passing the refresh token

<!-- Sessions -->

POST http://127.0.0.1:8000/api/sessions/create/ – Create a session (Instructor only)
-> Get the access token and paste it in Api's header Key: Authorization and value as: Bearer accesstoken 
PUT http://127.0.0.1:8000/api/sessions/19/update/ - Update the session(Only instructor)

DEL http://127.0.0.1:8000/api/sessions/19/delete/ - Delete the session (Only Instructor)

GET http://127.0.0.1:8000/api/public/sessions/ - All Upcoming session (Public)

GET http://127.0.0.1:8000/api/sessions/instructor/ – List instructor’s sessions

GET http://127.0.0.1:8000/api/sessions/{id}/ – Get session details (instructor view)

GET http://127.0.0.1:8000/api/public/sessions/{id}/ – Public session 


demodata.json - This file includes All the demodata for testing


**Run Test**
python manage.py test session

**Improvements**

-> Add celery to background task automation like (Email notification before 1 hr of the session)
-> Implementing cache
-> Logout, Reset pw

**Thank you for visiting**

