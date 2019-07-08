from django.urls import include, path
from .views import signup, logout_user, Login

app_name = "users"
urlpatterns = [
    path("signup", signup, name="signup"),
    path("logout", logout_user, name="logout"),
    path("login", Login.as_view(), name="login")
]
