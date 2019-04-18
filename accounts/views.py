from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

# Create your views here.
def signup(request):
    if request.user.is_authenticated:
        return redirect('boards:list')
        
    if request.method == 'POST':
        signup_form = UserCreationForm(request.POST)
        if signup_form.is_valid():
            user = signup_form.save()
            auth_login(request, user)
            return redirect('boards:list')
    else:
        signup_form = UserCreationForm()
    ctx = {
        'form': signup_form,
    }
    return render(request, 'accounts/form.html', ctx)

def login(request):
    if request.method == 'POST':
        login_form = AuthenticationForm(request.POST)
        if login_form.is_valid():
            auth_login(request, login_form.get_user())
            return redirect(request.GET.get('next') or 'boards:list')
    else:
        login_form = AuthenticationForm()
    ctx = {
        'form': login_form,
    }
    return render(request, 'accounts/form.html', ctx)

@login_required
@require_POST
def logout(request):
    return redirect('boards:list')