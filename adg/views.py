from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect


class CustomLoginView(LoginView):
    # if logged in redirects to next_page which is games page
    redirect_authenticated_user = True
    template_name = "registration/login.html"



def register(request):
    # TODO https://trello.com/c/QeuoeR54/282-login-page-if-already-logged-in-redirect-to-games-page
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
