from django.shortcuts import render, redirect

# Create your views here.
def home(request):
    user = request.user
    if(user.is_authenticated):
        return render(request, "core/index.html")
    else:
        return redirect('user-login')