from django.shortcuts import render, redirect
from .models import *

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

def delete_transaction(request,id):
    tracking_history = TrackingHistory.objects.filter(id=id)
    if tracking_history.exists():
        current_balance, _ = CurrentBalance.objects.get_or_create(id = 1)
        tracking_history = tracking_history[0]
        
        current_balance.current_balance = current_balance.current_balance - tracking_history.amount

        current_balance.save()


    tracking_history.delete()

    return redirect('/')