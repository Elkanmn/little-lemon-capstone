LITTLE LEMON RESTAURANT — DJANGO REST API
=========================================

Repository: upload this project to your own GitHub repository before peer review.
Environment setup: follow README.md. The production/course configuration uses MySQL.

API PATHS FOR PEER REVIEW
-------------------------
GET     /                           Django-rendered static HTML page
GET     /api/health/                Health check (public)
GET     /api/menu/                  List menu items (public)
GET     /api/menu/<id>/             Retrieve menu item (public)
POST    /api/menu/                  Create menu item (staff only)
PUT     /api/menu/<id>/             Replace menu item (staff only)
PATCH   /api/menu/<id>/             Modify menu item (staff only)
DELETE  /api/menu/<id>/             Delete menu item (staff only)
POST    /api/registration/          Register user, receive token
POST    /api/token/                 Login: receive token
POST    /api/logout/                Revoke current token
GET     /api/bookings/              List own bookings (staff: all)
POST    /api/bookings/              Create booking (authenticated)
GET     /api/bookings/<id>/         Retrieve own booking (staff: any)
PUT     /api/bookings/<id>/         Update own booking (staff: any)
PATCH   /api/bookings/<id>/         Partially update own booking
DELETE  /api/bookings/<id>/         Delete own booking (staff: any)

COURSEWORK ALIASES
------------------
GET/POST                /restaurant/menu/
GET/PUT/PATCH/DELETE    /restaurant/menu/<id>/
GET/POST                /restaurant/booking/tables/
GET/PUT/PATCH/DELETE    /restaurant/booking/tables/<id>/
POST                    /restaurant/api-token-auth/

REQUIRED AUTHENTICATION
-----------------------
Register: POST /api/registration/ with JSON:
{"username":"student1", "email":"student1@example.com", "password":"SecurePass479!"}

Token login: POST /api/token/ with JSON:
{"username":"student1", "password":"SecurePass479!"}

For authenticated endpoints add HTTP header:
Authorization: Token YOUR_TOKEN_HERE

Booking JSON example (use a FUTURE date):
{"name":"Amina", "email":"amina@example.com", "no_of_guests":4,
 "booking_date":"2027-02-12", "booking_time":"19:30:00", "special_requests":"Window seat"}

Menu JSON example for staff:
{"title":"Fresh Pasta", "description":"Pasta with lemon", "price":"17.00", "inventory":12, "category":"Main"}

Peer reviewers: install requirements, start the MySQL service, migrate, create
superuser, seed_menu, runserver, then import insomnia/LittleLemon_Insomnia.json.
See README.md for exact commands. Never commit .env or database credentials.
