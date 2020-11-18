from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignUpForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        print(request.POST)
        if form.is_valid():
            form.save()
            print('####################### # SAVED # ###########################')
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
        else:
            print('form is not valid')
            print(form.errors)
            messages.error(request, 'Error occured')
            return render(request, 'userauth/signup.html', {'form': form})
        return redirect('name_login_req')
    else:
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
        print(data)
        print(firstname)
        print(lastname)
        print(about)
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