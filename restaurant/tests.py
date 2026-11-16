from datetime import timedelta
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from .models import Booking, MenuItem

User = get_user_model()


def booking_payload():
    return {
        "name": "Amina", "email": "amina@example.com", "no_of_guests": 4,
        "booking_date": str(timezone.localdate() + timedelta(days=2)),
        "booking_time": "19:30:00", "special_requests": "Near the window",
    }


class PageAndHealthTests(TestCase):
    def test_html_home(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Little Lemon")

    def test_health(self):
        response = self.client.get(reverse("health"))
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"status": "ok", "application": "Little Lemon"})


class MenuAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="member", password="StrongPass123!")
        self.staff = User.objects.create_user(username="manager", password="StrongPass123!", is_staff=True)
        self.item = MenuItem.objects.create(title="Greek Salad", description="Fresh salad", price="12.50", inventory=10)
        self.payload = {"title": "Lemon Pasta", "description": "Fresh pasta", "price": "17.00", "inventory": 8, "category": "Main"}

    def test_anonymous_can_list_and_view_menu(self):
        self.assertEqual(self.client.get(reverse("menu-list")).status_code, status.HTTP_200_OK)
        self.assertEqual(self.client.get(reverse("menu-detail", args=[self.item.id])).status_code, status.HTTP_200_OK)

    def test_anonymous_cannot_create(self):
        self.assertEqual(self.client.post(reverse("menu-list"), self.payload).status_code, status.HTTP_401_UNAUTHORIZED)

    def test_regular_user_cannot_create(self):
        self.client.force_authenticate(user=self.user)
        self.assertEqual(self.client.post(reverse("menu-list"), self.payload).status_code, status.HTTP_403_FORBIDDEN)

    def test_staff_can_create_modify_and_delete(self):
        self.client.force_authenticate(user=self.staff)
        create = self.client.post(reverse("menu-list"), self.payload)
        self.assertEqual(create.status_code, status.HTTP_201_CREATED)
        url = reverse("menu-detail", args=[create.data["id"]])
        changed = self.client.patch(url, {"price": "18.00"})
        self.assertEqual(changed.status_code, status.HTTP_200_OK)
        self.assertEqual(self.client.delete(url).status_code, status.HTTP_204_NO_CONTENT)

    def test_alias_url_works(self):
        self.assertEqual(self.client.get(reverse("restaurant-menu-list")).status_code, status.HTTP_200_OK)

    def test_negative_price_is_invalid(self):
        self.client.force_authenticate(user=self.staff)
        bad = dict(self.payload, price="-1.00")
        self.assertEqual(self.client.post(reverse("menu-list"), bad).status_code, status.HTTP_400_BAD_REQUEST)


class RegistrationAndTokenTests(APITestCase):
    def test_register_and_login(self):
        registration = self.client.post(reverse("registration"), {
            "username": "newguest", "email": "guest@example.com", "password": "SecurePass479!"
        })
        self.assertEqual(registration.status_code, status.HTTP_201_CREATED)
        self.assertTrue(registration.data["token"])
        login = self.client.post(reverse("token"), {"username": "newguest", "password": "SecurePass479!"})
        self.assertEqual(login.status_code, status.HTTP_200_OK)
        self.assertEqual(login.data["token"], registration.data["token"])

    def test_short_password_is_rejected(self):
        response = self.client.post(reverse("registration"), {"username": "newguest", "password": "123"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_duplicate_username_is_rejected(self):
        User.objects.create_user(username="already", password="SecurePass479!")
        response = self.client.post(reverse("registration"), {"username": "already", "password": "SecurePass479!"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_logout_revokes_token(self):
        user = User.objects.create_user(username="guest", password="SecurePass479!")
        token = Token.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
        self.assertEqual(self.client.post(reverse("logout")).status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Token.objects.filter(user=user).exists())


class BookingAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="guest1", password="StrongPass123!")
        self.other = User.objects.create_user(username="guest2", password="StrongPass123!")
        self.staff = User.objects.create_user(username="manager", password="StrongPass123!", is_staff=True)
        self.booking = Booking.objects.create(user=self.user, **booking_payload())

    def test_anonymous_booking_rejected(self):
        self.assertEqual(self.client.get(reverse("booking-list")).status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(self.client.post(reverse("booking-list"), booking_payload()).status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_can_create_booking(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse("booking-list"), booking_payload())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Booking.objects.get(pk=response.data["id"]).user, self.user)

    def test_user_sees_own_bookings_only(self):
        self.client.force_authenticate(user=self.other)
        self.assertEqual(self.client.get(reverse("booking-list")).data, [])
        self.assertEqual(self.client.get(reverse("booking-detail", args=[self.booking.pk])).status_code, status.HTTP_404_NOT_FOUND)

    def test_owner_can_update_and_delete(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("booking-detail", args=[self.booking.pk])
        self.assertEqual(self.client.patch(url, {"no_of_guests": 6}).status_code, status.HTTP_200_OK)
        self.booking.refresh_from_db()
        self.assertEqual(self.booking.no_of_guests, 6)
        self.assertEqual(self.client.delete(url).status_code, status.HTTP_204_NO_CONTENT)

    def test_staff_can_view_all(self):
        self.client.force_authenticate(user=self.staff)
        response = self.client.get(reverse("booking-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_bad_guest_count_is_rejected(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse("booking-list"), dict(booking_payload(), no_of_guests=0))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_past_date_is_rejected(self):
        self.client.force_authenticate(user=self.user)
        date = str(timezone.localdate() - timedelta(days=2))
        response = self.client.post(reverse("booking-list"), dict(booking_payload(), booking_date=date))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_coursework_alias(self):
        self.client.force_authenticate(user=self.user)
        self.assertEqual(self.client.get(reverse("restaurant-booking-list")).status_code, status.HTTP_200_OK)
