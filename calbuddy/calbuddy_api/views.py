from rest_framework import permissions, generics, serializers
from django.contrib.auth.models import Group
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model, logout
from .models import Day, Meal
from .utils import fetch_calorie_data
from .paginations import CustomPagination
from datetime import date
from django.utils.decorators import method_decorator
from .mixins import GroupRequiredMixin


from . import serializers


class CreateUserView(generics.CreateAPIView):
    model = get_user_model()
    serializer_class = serializers.UserSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.model.objects.create_user(**serializer.validated_data)
        normal_users_group = Group.objects.get(name="Normal Users")
        user.groups.add(normal_users_group)
        user.save()
        return Response({"message": "User created sucessfully"}, status=201)


class LoginView(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(email=email, password=password)
        if user is None:
            return Response({"error": "Invalid username or password."}, status=401)

        login(request, user)
        return Response({"message : login successful"}, status=200)


class LogoutView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        logout(request)
        return Response({"message": "Successfully logged out."}, status=200)


class ViewProfileView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.UserSerializer

    def get(self, request):
        serializer = self.serializer_class(request.user)
        user_data = serializer.data
        del user_data["password"]
        return Response(user_data, status=200)


class EditProfileView(generics.UpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.UserSerializer

    def put(self, request):
        if request.data is None:
            return Response({"error": "No data was provided."}, status=400)
        if request.data.get("email") is not None:
            return Response({"error": "You cannot change your email."}, status=400)
        if request.data.get("password") is not None:
            return Response(
                {"error": "You cannot change your password using this endpoint."},
                status=400,
            )
        serializer = self.serializer_class(
            request.user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                "updated_data": serializer.data,
                "message": "Successfully updated profile.",
            },
            status=200,
        )


class DeleteAccountView(generics.DestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.UserSerializer

    def delete(self, request):
        request.user.delete()
        logout(request)
        return Response({"message": "Successfully deleted account."}, status=200)


class AddMealView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.MealSerializer

    def post(self, request):
        user = request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        meal_data = serializer.validated_data

        if meal_data.get("calories") is None:
            calories = fetch_calorie_data(meal_data.get("ingredients"))
            meal_data["calories"] = calories
        try:
            day = Day.objects.get(user=user, date=date.today())
        except Day.DoesNotExist:
            day = Day.objects.create(user=user, date=date.today())

        if meal_data.get("calories") + day.calories_consumed > user.daily_calorie_mark:
            meal_data["within_calorie_limit"] = False
        day.calories_consumed += meal_data.get("calories")
        day.save()
        Meal.objects.create(user=user, **meal_data)
        return Response({"message": "Meal added successfully"}, status=201)


class ListMealsView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.MealSerializer
    pagination_class = CustomPagination

    def get(self, request):
        user = request.user
        meals = Meal.objects.filter(user=user)
        date = self.request.query_params.get("date")
        if date is not None:
            meals = meals.filter(date=date)
        meals = self.paginate_queryset(meals)
        serializer = self.serializer_class(meals, many=True)
        if serializer.data == []:
            return Response({"message": "No meals found"}, status=404)
        return Response(serializer.data, status=200)


class AddUserView(GroupRequiredMixin, generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.UserSerializer
    model = get_user_model()
    group_required = ["User Manager", "Admin User"]

    def post(self, request):
        body = request.data
        group_name = body.get("group", "Normal Users")
        group_names = Group.objects.all().values_list("name", flat=True)
        if group_name not in group_names:
            return Response({"error": "Invalid group name"}, status=400)
        del body["group"]
        serializer = self.get_serializer(data=body)
        serializer.is_valid(raise_exception=True)
        user = self.model.objects.create_user(**serializer.validated_data)
        group = Group.objects.get(name=group_name)
        user.groups.add(group)
        user.save()
        return Response({"message": "User created sucessfully"}, status=201)


class ListUsersView(GroupRequiredMixin, generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.UserSerializer
    model = get_user_model()
    group_required = ["User Manager", "Admin User"]
    pagination_class = CustomPagination

    def get(self, request):
        users = self.model.objects.all()
        date_joined = self.request.query_params.get("date_joined")
        if date_joined is not None:
            users = users.filter(date_joined=date_joined)
        users = self.paginate_queryset(users)
        serializer = self.serializer_class(users, many=True)
        if serializer.data == []:
            return Response({"message": "No users found"}, status=404)
        return Response(serializer.data, status=200)


class EditUserDataView(GroupRequiredMixin, generics.UpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.UserSerializer
    model = get_user_model()
    group_required = ["User Manager", "Admin User"]

    def put(self, request):
        if request.data.get("email") is None:
            return Response({"error": "No email was provided."}, status=400)
        try:
            user = self.model.objects.get(email=request.data.get("email"))
        except self.model.DoesNotExist:
            return Response({"error": "User does not exist"}, status=404)
        body = request.data
        del body["email"]
        group_name = body.get("group", None)
        if group_name is not None:
            group_names = Group.objects.all().values_list("name", flat=True)
            if group_name not in group_names:
                return Response({"error": "Invalid group name"}, status=400)
            del body["group"]
        serializer = self.get_serializer(data=body, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        if group_name is not None:
            group = Group.objects.get(name=group_name)
            user.groups.add(group)
        return Response({"message": "User created sucessfully"}, status=201)


class DeleteUserView(GroupRequiredMixin, generics.DestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    model = get_user_model()
    group_required = ["User Manager", "Admin User"]

    def delete(self, request):
        if request.data.get("email") is None:
            return Response({"error": "No email was provided."}, status=400)
        try:
            user = self.model.objects.get(email=request.data.get("email"))
        except self.model.DoesNotExist:
            return Response({"error": "User does not exist"}, status=404)
        user.delete()
        return Response({"message": "Successfully deleted user."}, status=200)


class AddUserMealView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.MealSerializer
    group_required = ["Admin User"]
    model = get_user_model()

    def post(self, request):
        email = request.query_params.get("email")
        if email is None:
            return Response(
                {"error": "please provide email in url parameters"}, status=400
            )
        try:
            user = self.model.objects.get(email=email)
        except self.model.DoesNotExist:
            return Response({"error": "User does not exist"}, status=404)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        meal_data = serializer.validated_data
        if meal_data.get("calories") is None:
            calories = fetch_calorie_data(meal_data.get("ingredients"))
            meal_data["calories"] = calories
        try:
            day = Day.objects.get(user=user, date=date.today())
        except Day.DoesNotExist:
            day = Day.objects.create(user=user, date=date.today())

        if meal_data.get("calories") + day.calories_consumed > user.daily_calorie_mark:
            meal_data["within_calorie_limit"] = False
        day.calories_consumed += meal_data.get("calories")
        day.save()
        Meal.objects.create(user=user, **meal_data)
        return Response(
            {"message": f"Meal added successfully for user: {user.email}"}, status=201
        )
