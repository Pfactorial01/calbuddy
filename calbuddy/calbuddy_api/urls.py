from django.urls import path
from rest_framework import routers
from .views import (
    CreateUserView,
    LoginView,
    LogoutView,
    ViewProfileView,
    EditProfileView,
    DeleteAccountView,
    AddMealView,
    ListMealsView,
    AddUserView,
    EditUserDataView,
    DeleteUserView,
    ListUsersView,
    AddUserMealView,
)

app_name = "calbuddy_api"
router = routers.DefaultRouter()

urlpatterns = [
    path("register/", CreateUserView.as_view()),
    path("login/", LoginView.as_view()),
    path("logout/", LogoutView.as_view()),
    path("view_profile/", ViewProfileView.as_view()),
    path("edit_profile/", EditProfileView.as_view()),
    path("delete_account/", DeleteAccountView.as_view()),
    path("add_meal/", AddMealView.as_view()),
    path("list_meals/", ListMealsView.as_view()),
    path("create_user/", AddUserView.as_view()),
    path("edit_user_data/", EditUserDataView.as_view()),
    path("delete_user/", DeleteUserView.as_view()),
    path("list_users/", ListUsersView.as_view()),
    path("add_user_meal/", AddUserMealView.as_view()),
]
