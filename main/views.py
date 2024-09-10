
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import UserRegisterForm, LoginForm
from .models import User

def login_view(request):

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            print(email, password)
            user = authenticate(request, username=email, password=password)

            if user is not None:
                login(request, user, backend='main.auth_backends.EmailBackend')


                if user.company_code == "telegram":
                    return redirect('index1')
                elif user.company_code == 'site':
                    return redirect('index')
                else:
                    return redirect('default_index')
            else:

                return render(request, 'signin.html', {'form': form, 'invalid': True})
    else:
        form = LoginForm()

    return render(request, 'signin.html', {'form': form, 'invalid': False})

def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'signup.html', {'form': form})




def logout_view(request):
    logout(request)
    return redirect('login')










