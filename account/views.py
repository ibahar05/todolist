from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login, logout


class TodoLoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, "account/login.html",{"form":form})

    def post(self,request):
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request,username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("todo:todo")
        
        form = AuthenticationForm()
        return render(request, "account/login.html", {
            "form": form, 
            "error": "نام کاربری یا رمز عبور اشتباه است."
        })
        

class TodoRegisterView(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, "account/register.html")
    
    def post(self, request):
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user) 
            return redirect("todo:todo") 
            
        return render(request, "account/register.html", {"form": form})
    

class LogoutView(View):
    def post(self, request):
        logout(request) 
        return redirect('account:login')
