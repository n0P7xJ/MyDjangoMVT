from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    # код view
    return render(request, 'home.html')

def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, "registration/register.html", {"form": form})
