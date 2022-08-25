from accounts.views import LoginAPI, RegisterAPI, UserAPI, UsersListView
from django.urls import path


urlpatterns = [
	path("login/", LoginAPI.as_view()),
	path("register/", RegisterAPI.as_view()),
	path("user/", UserAPI.as_view()),
    path("users/", UsersListView.as_view())
]