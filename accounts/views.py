from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout
)
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect

from .forms import UserLoginForm, UserRegisterForm


def register_view(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')

    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        login(request, user)

        return redirect('/')

    context = {
        'form': form,
        'page_title': 'Register'
    }
    return render(request, 'form.html', context)


def login_view(request):

    if request.user.is_authenticated():
        return redirect('/')

    redirect_url = request.GET.get('next')

    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')

        user = authenticate(username=username, password=password)
        login(request, user)

        if redirect_url:
            return redirect(redirect_url)
        return redirect('/')

    context = {
        'form': form,
        'page_title': 'Login'
    }
    return render(request, 'form.html', context)


def logout_view(request):
    logout(request)
    return redirect('/')
