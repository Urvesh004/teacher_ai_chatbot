from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages

from admin_panel.models import UserLog
from .forms import RegisterForm


def login_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user:

            login(request, user)

            # Create User Log
            UserLog.objects.create(
                user=user,
                activity="LOGIN"
            )

            if user.role == "superadmin":
                return redirect("/admin-panel/")

            return redirect("home")

        messages.error(
            request,
            "Invalid username or password"
        )

    return render(
        request,
        "excel_ai_chatbot/login.html"
    )


def register_view(request):

    form = RegisterForm()

    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():

            user= form.save()
            
            UserLog.objects.create(user=user, activity="REGISTER")

            messages.success(request, "Account Created Successfully")

            return redirect("login")

    return render(request, "excel_ai_chatbot/register.html", {"form": form})


def logout_view(request):

    if request.user.is_authenticated:

        UserLog.objects.create(
            user=request.user,
            activity="LOGOUT"
        )

    logout(request)

    return redirect("login")