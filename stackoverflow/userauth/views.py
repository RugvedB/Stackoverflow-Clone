from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignUpForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.urls import reverse
from django.http import HttpResponse
from django.template.loader import render_to_string
from .tokens import account_activation_token
User = get_user_model()

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            mail_subject = 'Activate your Stackoberflow account.'
            message = render_to_string('userauth/user_active_email.html', {
                'user': user.username,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            username = form.cleaned_data.get('username')
            messages.success(request, f"New account created: {username}, Please confirm your email address to complete the registration")
            return redirect("/")
        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")
            return render(request = request, template_name = "userauth/signup.html", context={"form":form})
        
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

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request, 'Account activated successfully. Thank you for your email confirmation. Now you can login your account.')
        return redirect('name_login_req')
    else:
        messages.error(request, 'Activation link is invalid!')
        return redirect('name_login_req')