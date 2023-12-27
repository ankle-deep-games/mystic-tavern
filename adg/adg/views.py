from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect


def login_user(request):
    return render(request, 'registration/login.html', {})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            if len(username) > 7:
                messages.error(
                    request, "Username must be 7 characters or less.", extra_tags="alert alert-danger"
                )
                return redirect("register")

            password = form.cleaned_data['password1']

            form.save()

            user = authenticate(username=username, password=password)
            login(request, user)

            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            else:
                return redirect("tavern_app:games")
    else:
        form = UserCreationForm()

    return render(request, 'registration/register.html', {'form': form})
