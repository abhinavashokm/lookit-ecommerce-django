from django.shortcuts import render, redirect

# Create your views here.
def home(request):
    user = request.user
    if(user.is_authenticated):
        return render(request, "core/index.html",{user:user})
    else:
        return redirect('user-login')