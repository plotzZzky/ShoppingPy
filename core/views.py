from django.shortcuts import render, redirect


def home(request):
    return redirect('/list/')


def about(request):
    return render(request, 'about.html')


