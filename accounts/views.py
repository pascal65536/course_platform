from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


def custom_logout(request):
    if request.method == "POST":
        logout(request)
        return redirect("course_page")
    else:
        return redirect("course_page")


def custom_login(request):
    form = AuthenticationForm()
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect("course_page")
                else:
                    messages.info(request, "This account is inactive.")
            else:
                msg = "Please enter a correct username and password. Note that both fields may be case-sensitive."
                messages.info(request, msg)
        # else:
        #     for field in form:
        #         for error in field.errors:
        #             messages.error(request, f"{field.name}: {error}")
        #     for error in form.non_field_errors():
        #         messages.error(request, error)       
    return render(request, "login.html", {"form": form})


def register(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("course_page")       
    return render(request, "register.html", {"form": form})


@login_required
def profile(request):
    return render(request, "profile.html", {"user": request.user})
