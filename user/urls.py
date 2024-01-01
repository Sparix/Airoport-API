from django.urls import path

from user.views import CreateUserView, CreateTokenView, ProfileUserView

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="register"),
    path("login/", CreateTokenView.as_view(), name="login"),
    path("profile/", ProfileUserView.as_view(), name="profile"),
]

app_name = "user"
