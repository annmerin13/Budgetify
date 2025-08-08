from django.shortcuts import render,redirect
from .models import *
from Admin.models import *
from User.models import *

import random
from datetime import datetime, timedelta
from django.utils import timezone


# Create your views here.

def userregistration(request):
    if request.method=="POST":
        tbl_user.objects.create(
            user_name=request.POST.get("txt_name"),
            user_email=request.POST.get("txt_email"),
            user_password=request.POST.get("txt_password")
            )
        return render(request,"Guest/Userregistration.html",{"msg":"Inserted Successfully"})
    else:
        return render(request,"Guest/Userregistration.html")
    
def Login(request):
    if request.method == "POST":
        usercount = tbl_user.objects.filter(user_email=request.POST.get("txt_email"),user_password=request.POST.get("txt_password")).count()
        #admincount = tbl_adminregistration.objects.filter(admin_email=request.POST.get("txt_email"),admin_password=request.POST.get("txt_password")).count()
        if usercount > 0:
            user = tbl_user.objects.get(user_email=request.POST.get("txt_email"),user_password=request.POST.get("txt_password"))
            #generate_demo_data(user, months=6)

            request.session["uid"] = user.id
            return redirect("User:homepage")
        # elif admincount > 0:
        #     admin = tbl_adminregistration.objects.get(admin_email=request.POST.get("txt_email"),admin_password=request.POST.get("txt_password"))
        #     request.session["aid"] = admin.id
        #     return redirect("Admin:homepage")
        else:
            return render(request,"Guest/Login.html",{"msg":"Invalid Email Or Password"})
    else:
        return render(request,"Guest/Login.html")

def LoginAdmin(request):
    if request.method == "POST":
        admincount = tbl_adminregistration.objects.filter(admin_email=request.POST.get("txt_email"),admin_password=request.POST.get("txt_password")).count()
        if admincount > 0:
            admin = tbl_adminregistration.objects.get(admin_email=request.POST.get("txt_email"),admin_password=request.POST.get("txt_password"))
            request.session["aid"] = admin.id
            return redirect("Admin:homepage")
        else:
            return render(request,"Guest/Login.html",{"msg":"Invalid Email Or Password"})
    else:
        return render(request,"Guest/Login.html")


def index(request):
    return render(request,"Guest/index.html")
































def generate_demo_data(user, months=6):
    """
    Generate exactly 100 records for each data type over 6 months
    """
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=30 * months)
    total_days = (end_date - start_date).days
    
    # Manual income types
    income_types = [
        tbl_incometype.objects.get_or_create(incometype_name=name)[0]
        for name in ['Salary', 'Bonus', 'Investment Returns']
    ]
    
    # Manual expense types
    expense_types = [
        tbl_expensetype.objects.get_or_create(expensetype_name=name)[0]
        for name in ['Food', 'Utilities', 'Travel']
    ]
    
    # Manual data lists
    income_notes = ['Monthly pay', 'Project completion', 'Dividend payment']
    expense_notes = ['Grocery shopping', 'Electricity bill', 'Bus fare']
    saving_titles = ['House Fund', 'Vacation Fund', 'Emergency Fund']
    repayment_names = ['Car Loan', 'Personal Loan', 'Equipment Financing']
    notification_titles = ['Loan Payment', 'Installment Due', 'Repayment Reminder']
    notification_descs = ['Monthly payment due', 'Please pay on time', 'Upcoming due date']
    statuses = ['Pending', 'Paid', 'Overdue']
    
    # Generate 100 income records
    for i in range(100):
        days_offset = (total_days * i) // 100  # Evenly distribute over 6 months
        tbl_income.objects.create(
            income_amount=round(random.uniform(1000, 10000), 2),
            income_date=start_date + timedelta(days=days_offset),
            income_note=random.choice(income_notes),
            incomecategory=random.choice(income_types),
            user=user
        )
    
    # Generate 100 expense records
    for i in range(100):
        days_offset = (total_days * i) // 100
        tbl_expense.objects.create(
            expense_amount=round(random.uniform(50, 1000), 2),
            expense_date=start_date + timedelta(days=days_offset),
            expense_time=timezone.now().replace(
                hour=random.randint(0, 23),
                minute=random.randint(0, 59),
                second=0,
                microsecond=0
            ).time(),
            expense_note=random.choice(expense_notes),
            expense_bill=f'Assets/ExpenseBill/Bill_{i % 5 + 1}.png',
            expensecategory=random.choice(expense_types),
            user=user
        )
    
    # Generate 100 budget records
    expense_type_cycle = len(expense_types)
    for i in range(100):
        days_offset = (total_days * i) // 100
        tbl_budget.objects.create(
            budget_amount=round(random.uniform(500, 2000), 2),
            user=user,
            expensecategory=expense_types[i % expense_type_cycle],
            date_added=start_date + timedelta(days=days_offset)
        )
    
    # Generate 100 saving heads
    saving_heads = []
    for i in range(100):
        days_offset = (total_days * i) // 100
        head = tbl_savinghead.objects.create(
            savinghead_title=random.choice(saving_titles),
            savinghead_goal=str(round(random.uniform(10000, 100000), 2)),
            savinghead_date=start_date + timedelta(days=days_offset),
            user=user
        )
        saving_heads.append(head)
    
    # Generate 100 saving body records
    for i in range(100):
        head = saving_heads[i]  # Use corresponding saving head
        tbl_savingbody.objects.create(
            savingbody_amount=round(random.uniform(500, 2000), 2),
            savingbody_date=head.savinghead_date + timedelta(days=random.randint(0, 30)),
            savinghead=head
        )
    
    # Generate 100 repayments
    for i in range(100):
        days_offset = (total_days * i) // 100
        tbl_repayment.objects.create(
            repayment_amount=str(round(random.uniform(1000, 50000), 2)),
            repayment_date=start_date + timedelta(days=days_offset),
            repayment_tenure=f'Assets/TenureBill/Tenure_{i % 5 + 1}.png',
            repayment_name=random.choice(repayment_names),
            user=user
        )
    
    # Generate 100 repayment notifications
    for i in range(100):
        days_offset = (total_days * i) // 100
        payment_date = start_date + timedelta(days=days_offset + random.randint(1, 30))
        tbl_repaymentnotification.objects.create(
            repaymentnotification_title=random.choice(notification_titles),
            repaymentnotification_description=random.choice(notification_descs),
            repaymentnotification_amount=str(round(random.uniform(100, 2000), 2)),
            repaymentnotification_notificationdate=random.randint(1, 7),
            repaymentnotification_paymentdate=payment_date.strftime('%Y-%m-%d'),
            repaymentnotification_status=random.choice(statuses),
            user=user,
            last_acknowledged_date=payment_date if random.choice([True, False]) else None
        )

def daterange(start_date, end_date, delta_days):
    """Generate dates from start_date to end_date with delta_days steps"""
    current_date = start_date
    while current_date < end_date:
        yield current_date
        current_date += timedelta(days=delta_days)