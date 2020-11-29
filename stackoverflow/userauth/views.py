from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignUpForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"New account created: {username}")
            login(request, user)
            messages.info(request, f"You are logged in as {username}")
            return redirect("/")
        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")
            return render(request = request, template_name = "main/signup.html", context={"form":form})
        
    form = SignUpForm()
    return render(request, 'userauth/signup.html', {'form': form})

@login_required
def editprofile(request):
    user = request.user
    if request.method == 'POST':
        data = request.POST.dict()
        firstname = data.get('firstname')
        lastname = data.get('lastname')
        about = data.get('about')
        if firstname != '':
            user.first_name = firstname
        if lastname != '':
            user.last_name = lastname
        if about != '':
            user.about_me = about
        if request.FILES and request.FILES['fileInput']:
            user.profile_pic = request.FILES['fileInput']
        user.save()
        messages.success(request, 'Profile updated successfully')
    return render(request, 'userauth/editprofile.html', {'user':user})

@login_required
def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!" )
    return redirect("/")



def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data = request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are logged in as {username}")
                return redirect("/")
            else:
                messages.error(request, "Invalid username or password")
                        
        else:
            messages.error(request, "Invalid username or password")
            
    form  =  AuthenticationForm()
    return render(request, "userauth/login.html", {"form" : form})