from django.contrib import admin
from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token
from restaurant import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("api/health/", views.health, name="health"),
    path("api/menu/", views.MenuViewSet.as_view({"get": "list", "post": "create"}), name="menu-list"),
    path("api/menu/<int:pk>/", views.MenuViewSet.as_view({"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"}), name="menu-detail"),
    path("api/bookings/", views.BookingViewSet.as_view({"get": "list", "post": "create"}), name="booking-list"),
    path("api/bookings/<int:pk>/", views.BookingViewSet.as_view({"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"}), name="booking-detail"),
    path("api/registration/", views.RegisterView.as_view(), name="registration"),
    path("api/token/", obtain_auth_token, name="token"),
    path("api/logout/", views.LogoutView.as_view(), name="logout"),

    # Friendly aliases matching Little Lemon coursework naming conventions.
    path("restaurant/menu/", views.MenuViewSet.as_view({"get": "list", "post": "create"}), name="restaurant-menu-list"),
    path("restaurant/menu/<int:pk>/", views.MenuViewSet.as_view({"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"}), name="restaurant-menu-detail"),
    path("restaurant/booking/tables/", views.BookingViewSet.as_view({"get": "list", "post": "create"}), name="restaurant-booking-list"),
    path("restaurant/booking/tables/<int:pk>/", views.BookingViewSet.as_view({"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"}), name="restaurant-booking-detail"),
    path("restaurant/api-token-auth/", obtain_auth_token, name="restaurant-token"),
    path("api-auth/", include("rest_framework.urls")),
]
