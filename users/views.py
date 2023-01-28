from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .forms import UserLoginForm, CustomUserCreationForm, EditUserForm
from .models import List, Pantry


def login_user(request):
    if request.user.is_authenticated:
        return redirect('/list/')
    else:
        if request.method == 'GET':
            login_form = UserLoginForm()
            signup_form = CustomUserCreationForm()
            return render(request, 'login.html', {'login': login_form, 'signup': signup_form})
        else:
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/list/')
            else:
                return redirect('/users/login')


def register_user(request):
    form = CustomUserCreationForm(request.POST)
    if form.is_valid():
        form.save()
        username = request.POST['username']
        password = request.POST['password1']
        user = authenticate(username=username, password=password)
        user_list = List(user=user)
        user_list.save()
        user_pantry = Pantry(user=user)
        user_pantry.save()
        if user is not None:
            login(request, user)
            return redirect('/list/')
    else:
        return redirect('/users/login')


@login_required()
def logout_user(request):
    logout(request)
    return redirect('/users/login')


@login_required()
def edit_user(request):
    if request.method == 'POST':
        form = EditUserForm(user=request.user, data=request.POST)
        if form.is_valid(user=request.user, data=request.POST):
            user = User.objects.get(pk=request.user.id)
            user.username = request.POST['username']
            user.email = request.POST['email']
            pwd = request.POST['password1']
            pwd2 = request.POST['password2']
            if pwd == pwd2 and pwd2 != '' and pwd != '':
                user.set_password(pwd)
                update_session_auth_hash(request, user)
            user.save()
            return redirect('/list/')
        else:
            data = {'form': form}
            print(form.errors)
            return render(request, 'edit.html', data)
    else:
        form = EditUserForm(user=request.user)
        data = {'form': form}
        return render(request, 'edit.html', data)
