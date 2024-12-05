from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

@login_required(login_url='login_view')
def index(request):

    current_balance, _ = CurrentBalance.objects.get_or_create(id=1)

    if request.method =="POST":
        amount = request.POST.get("amount")
        expense_type = "CREDIT"
        if float(amount)<0:
            expense_type = "DEBIT"
        description = request.POST.get("description")
        
        history = TrackingHistory.objects.create(
            current_balance =current_balance,
            amount =amount,
            expense_type = expense_type,
            description = description
        )

        current_balance.current_balance += float(amount)
        current_balance.save() 

        return redirect('/')
    
    income = 0.0
    expense = 0.0

    for history in TrackingHistory.objects.all():
        if history.expense_type == "CREDIT":
            income += history.amount
        elif history.expense_type == "DEBIT":
            expense += history.amount

    context = {
        "income" : income,
        "expense" : expense,
        "current_balance" :current_balance.current_balance,
        "transactions" : TrackingHistory.objects.all()
    }

    return render(request, 'index.html',context=context)

@login_required(login_url='login_view')
def delete_transaction(request,id):

    tracking_history = TrackingHistory.objects.filter(id=id)
    if tracking_history.exists():
        current_balance, _ = CurrentBalance.objects.get_or_create(id = 1)
        tracking_history = tracking_history[0]
        
        current_balance.current_balance = current_balance.current_balance - tracking_history.amount

        current_balance.save()


    tracking_history.delete()

    return redirect('/')

def login_view(request):
    if request.method == "POST":
        user_name = request.POST.get("user_name")
        password = request.POST.get("password")
        
        if User.objects.filter(username=user_name).exists():
            user = authenticate(username = user_name, password = password)
            if user:
                login(request, user=user)
                return redirect('/')
        
        messages.warning(request, "Username or password incorrect!")

        return redirect('login_view')
    return render(request, 'login.html')

def registration_view(request):
    if request.method == 'POST':
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        user_name = request.POST.get("user_name")
        password = request.POST.get("password")


        if User.objects.filter(username=user_name).exists():
            messages.warning(request, "User name already taken")
            return redirect('registration_view')
        
        user = User.objects.create(
            username = user_name,
            first_name = first_name,
            last_name = last_name,
        )
        user.set_password(password)
        user.save()
        messages.warning(request, "Account Created")
        print("User created")
        return redirect('registration_view')
    
    return render(request, 'registration.html')

@login_required(login_url='login_view')
def logout_view(request):
    logout(request)
    return redirect('login_view')

