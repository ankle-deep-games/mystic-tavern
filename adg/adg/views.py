from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login


def login_user(request):
    return render(request, 'registration/login.html', {})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            # Redirect to a success page, login page, or any other desired page
            return redirect("tavern_app:games")
    else:
        form = UserCreationForm()

    return render(request, 'registration/register.html', {'form': form})