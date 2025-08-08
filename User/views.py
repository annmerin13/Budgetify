from django.shortcuts import render,redirect
from Admin.models import *
from .models import *
from django.db.models import Sum, F, Q
from django.utils.timezone import now
from dateutil.relativedelta import relativedelta  # Import for adding months
import json
from django.utils import timezone
from django.http import HttpResponse
from reportlab.pdfgen import canvas
import csv
from datetime import datetime, timedelta
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.db.models import Sum, Count, F, Q
from django.utils.timezone import now
import json
from django.core.mail import send_mail
from django.conf import settings
from django.template import Template, Context




@csrf_exempt
def acknowledge_notification(request):
    if request.method == "POST":
        data = json.loads(request.body)
        notification_id = data.get("id")
        notification = tbl_repaymentnotification.objects.get(id=notification_id)
        notification.last_acknowledged_date = datetime.today().date()
        notification.save()
        return JsonResponse({"status": "success"})


def get_notifications(user_id):
    user=tbl_user.objects.get(id=user_id)

    today = datetime.today().date()
    notifications = []
    repayment_notifications = tbl_repaymentnotification.objects.filter(user_id=user_id)
    # email=repayment_notifications.user.user_email
    # print(email)
    for notification in repayment_notifications:
        # Parse the payment date
        payment_date = datetime.strptime(notification.repaymentnotification_paymentdate, "%Y-%m-%d").date()

        # Calculate the notification start date
        notification_days_before = int(notification.repaymentnotification_notificationdate)
        notification_start_date = payment_date - timedelta(days=notification_days_before)

        # Check if the current date is within the notification range
        if notification_start_date <= today < payment_date:
            # Check if the user has acknowledged the notification today
            if notification.last_acknowledged_date != today:
                notifications.append({
                    "id": notification.id,
                    "title": notification.repaymentnotification_title,
                    "description": notification.repaymentnotification_description,
                    "amount": notification.repaymentnotification_amount,
                    "payment_date": notification.repaymentnotification_paymentdate,
                    "notification_start_date": notification_start_date.strftime("%Y-%m-%d"),  # Format as YYYY-MM-DD
                })
                #user email
                email=user.user_email
               # Email content for bill payment reminder
                subject = "Respected Sir/Madam - Reminder: Upcoming Bill Payment Due"
                body = (
                    f"Dear {user.user_name},\r\n"  
                    "\r\n"
                    "Thank you for choosing us for your needs! We truly appreciate your continued trust in our services.\r\n"
                    "\r\n"
                    f"We would like to kindly remind you that your upcoming bill payment for '{notification.repaymentnotification_title}' is due soon. "
                    "To ensure uninterrupted service, please settle the outstanding amount at your earliest convenience.\r\n"
                    "\r\n"
                    "Payment Details:\r\n"
                    f"- Amount Due: {notification.repaymentnotification_amount}\r\n"
                    f"- Due Date: {notification.repaymentnotification_paymentdate}\r\n"
                    "- Payment Methods: Online portal, bank transfer, or contact support for more options\r\n"
                    "\r\n"
                    "Our team is committed to providing you with exceptional service, and we’re here to assist if you have any questions about your bill or payment process. "
                    "If you’ve already made the payment, please disregard this reminder.\r\n"
                    "\r\n"
                    "If you have any feedback or need support, feel free to reach out. Your input is important for us.\r\n"
                    "\r\n"
                    "Thank you for your prompt attention to this matter. We look forward to serving you again. Have a fantastic day!\r\n"
                    "\r\n"
                    "Best regards,\r\n"
                    "BUDGETIFY"
                )

                
                send_mail(
                    subject,  
                    body,     
                    settings.EMAIL_HOST_USER,  
                    [email],  
                    fail_silently=False, 
                )

    return notifications

# Create your views here.
def homepage(request):
    user_id = request.session.get("uid")
    notifications = get_notifications(user_id)

    return render(request,"User/Homepage.html",{"notifications": notifications})

def myprofile(request):
    user=tbl_user.objects.get(id=request.session["uid"])
    return render(request,"User/Myprofile.html",{"user":user})

def editprofile(request):
    user=tbl_user.objects.get(id=request.session["uid"])
    if request.method == 'POST':
        user_name = request.POST.get("txt_name")
        user_email = request.POST.get("txt_email")
        user.user_name=user_name
        user.user_email=user_email
        user.save()
        return render(request,"User/Editprofile.html",{"user":user})
    else:
        return render(request,"User/Editprofile.html",{"user":user})

def deleteComplaint(request,iid):
    tbl_complaint.objects.get(id=iid).delete()
    return redirect("User:complaint")
    
def complaint(request):
    user=tbl_user.objects.get(id=request.session["uid"])
    complaintData = tbl_complaint.objects.filter(user = user)
    if request.method=="POST":
        tbl_complaint.objects.create(
        complaint_title=request.POST.get('txt_title'),
        complaint_content=request.POST.get('txt_content'),
        #complaint_reply=request.POST.get('txt_reply'),
        user=tbl_user.objects.get(id=request.session["uid"])
        )
        return render(request,"User/Complaint.html",{"msg":"Inserted Successfully"})
    else:
        return render(request,"User/Complaint.html",{"complaintData":complaintData})

def reply(request,cid):
    if request.method=="POST":
        complaintData = tbl_complaint.objects.get(id=cid)
        replyData = request.POST.get("txt_reply")
        complaintData.complaint_reply=replyData
        complaintData.save()
        return redirect("Admin:Viewcomplaint.html")
    else:
        return render(request,"Admin/Reply.html")

        
def savinghead(request):
    user=tbl_user.objects.get(id=request.session["uid"])
    savingheadData = tbl_savinghead.objects.filter(user = user)
    
    if request.method == 'POST':
        tbl_savinghead.objects.create(
            savinghead_title=request.POST.get('txt_title'),
            savinghead_goal=request.POST.get('txt_goal'),
            user=tbl_user.objects.get(id=request.session["uid"])
        )
        return render(request,"User/Savinghead.html",{"msg":"Inserted Successfully"})
    else:
        return render(request,"User/Savinghead.html",{"savingheadData":savingheadData})

def deleteSavingHead(request,iid):
    tbl_savinghead.objects.get(id=iid).delete()
    return redirect("User:savinghead")

def budget(request):
    expensetypeData = tbl_expensetype.objects.all()
    user=tbl_user.objects.get(id=request.session["uid"])
    budgetData = tbl_budget.objects.filter(user = user)
    if request.method == 'POST':
        tbl_budget.objects.create(
            expensecategory=tbl_expensetype.objects.get(id=request.POST.get('txt_expensetype')),
            budget_amount=request.POST.get('txt_amount'),
            user=tbl_user.objects.get(id=request.session["uid"])
        )
        return render(request,"User/Budget.html",{"msg":"Inserted Successfully"})
    else:
        return render(request,"User/Budget.html",{"expensetypeData":expensetypeData,'budgetData':budgetData})
    
def deleteBudget(request,iid):
    tbl_budget.objects.get(id=iid).delete()
    return redirect("User:budget")
    
def savingbody(request,id):
    savingbodyData = tbl_savingbody.objects.filter(savinghead = id)
    if request.method == 'POST':
        tbl_savingbody.objects.create(
            savingbody_amount = request.POST.get('txt_amount'),
            savinghead = tbl_savinghead.objects.get(id=id)
        )
        return render(request,"User/Savingbody.html",{"msg":"Inserted Successfully"})
    else:
        return render(request,"User/Savingbody.html",{"savingbodyData":savingbodyData})
    
def income(request):
    incometypeData = tbl_incometype.objects.all()
    user=tbl_user.objects.get(id=request.session["uid"])
    incomeData = tbl_income.objects.filter(user = user)
    if request.method == 'POST':
        tbl_income.objects.create(
            incomecategory=tbl_incometype.objects.get(id=request.POST.get('txt_incometype')),
            income_note=request.POST.get('txt_note'),
            income_amount=request.POST.get('txt_amount'),
            user=tbl_user.objects.get(id=request.session["uid"])
        )
        return render(request,"User/Income.html",{"msg":"Inserted Successfully"})
    else:
        return render(request,"User/Income.html",{"incomeData":incomeData,'incometypeData':incometypeData})
    
def deleteIncome(request,iid):
    tbl_income.objects.get(id=iid).delete()
    return redirect("User:income")
  
def expense(request): 
    expensetypeData = tbl_expensetype.objects.all()
    user = tbl_user.objects.get(id=request.session["uid"])
    expenseData = tbl_expense.objects.filter(user=user)

    if request.method == 'POST':
        expensetype = tbl_expensetype.objects.get(id=request.POST.get('txt_expensetype'))
        expense_amount = float(request.POST.get('txt_amount'))  # Convert to float for comparison
        expense_note = request.POST.get('txt_note')
        # Get the latest budget for the selected expense type and user
        latest_budget = tbl_budget.objects.filter(expensecategory=expensetype, user=user).order_by('-id').first()
        
        # Default message
        msg = "Inserted Successfully"

        if latest_budget:
            budget_amount = float(latest_budget.budget_amount)  # Convert to float
            budget_start_date = latest_budget.date_added  # Ensure this field exists in tbl_budget
            budget_end_date = budget_start_date + relativedelta(months=1)  # Next month same date

            # Sum all expenses for this category within the budget period
            total_expense = tbl_expense.objects.filter(
                expensecategory=expensetype,
                user=user,
                expense_date__range=[budget_start_date, budget_end_date]
            ).aggregate(Sum('expense_amount'))['expense_amount__sum'] or 0

            # Check if adding this expense exceeds the budget
            if total_expense + expense_amount > budget_amount:
                tbl_expense.objects.create(
                    expensecategory=expensetype,
                    user=user,
                    expense_amount=expense_amount,
                    expense_bill=request.FILES.get('file_bill'),
                )
                return render(request, "User/Expense.html", {
                    "msg": "Expense exceeds the budget limit!",
                    "expenseData": expenseData,
                    "expensetypeData": expensetypeData
                })

            # Recalculate total expense after adding the new one
            total_expense_after = total_expense + expense_amount

            # Check if total expense reaches or exceeds 80% of the budget
            if total_expense_after >= (budget_amount * 0.8):
                # HTML email content with inline CSS
                html_content = Template("""
                <!DOCTYPE html>
                <html>
                <head>
                    <style>
                        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
                        .container { max-width: 600px; margin: 20px auto; padding: 20px; border: 1px solid #ddd; border-radius: 5px; background-color: #f9f9f9; }
                        .header { background-color: #FF9800; color: white; padding: 10px; text-align: center; border-radius: 5px 5px 0 0; }
                        .content { padding: 20px; background-color: white; border-radius: 0 0 5px 5px; }
                        .warning { color: #D32F2F; font-weight: bold; text-align: center; margin: 15px 0; }
                        .footer { text-align: center; font-size: 12px; color: #777; margin-top: 20px; }
                        .details { background-color: #f1f1f1; padding: 10px; border-left: 4px solid #FF9800; margin: 10px 0; }
                        a { color: #FF9800; text-decoration: none; }
                        a:hover { text-decoration: underline; }
                    </style>
                </head>
                <body>
                    <div class="container">
                        <div class="header">
                            <h2>Budget Usage Alert</h2>
                        </div>
                        <div class="content">
                            <p>Dear {{ username }},</p>
                            <p>We hope you’re doing well! This is a friendly reminder from <strong>BUDGETIFY</strong> regarding your budget for <strong>{{ category }}</strong>.</p>
                            <p>You’ve used <strong>{{ percentage }}%</strong> of your allocated budget for this category. Please review your spending to stay on track.</p>
                            <p>Smart Spending, Smarter Saving :) </p>
                            <div class="details">
                                <h3>Budget Details</h3>
                                <p><strong>Budget Amount:</strong> {{ budget_amount }}</p>
                                <p><strong>Total Spent:</strong> {{ total_spent }}</p>
                                <p><strong>Period:</strong> {{ start_date }} to {{ end_date }}</p>
                            </div>
                            <p class="warning">You’re approaching your budget limit!</p>
                            <p>Thank you for choosing BUDGETIFY!</p>
                            <p>Best regards,<br><strong>Team Budgetify</strong></p>
                        </div>
                        <div class="footer">
                            <p>© 2025 BUDGETIFY. All rights reserved.</p>
                        </div>
                    </div>
                </body>
                </html>
                """)

                # Calculate percentage
                percentage_used = (total_expense_after / budget_amount) * 100

                # Render the template with dynamic data
                context = {
                    "username": user.user_name,  
                    "category": expensetype.expensetype_name,  
                    "percentage": round(percentage_used, 2),
                    "budget_amount": budget_amount,
                    "total_spent": total_expense_after,
                    "start_date": budget_start_date.strftime("%Y-%m-%d"),
                    "end_date": budget_end_date.strftime("%Y-%m-%d"),
                }
                rendered_html = html_content.render(Context(context))

                # Send the email
                send_mail(
                    subject="Budget Alert: 80% of Your Budget Used",
                    message="Dear {},\n\nYou’ve used 80% of your budget for {}. Please check your email in HTML for details.".format(user.user_name, expensetype.expensetype_name),
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[user.user_email],  # Assuming user_email exists in tbl_user
                    html_message=rendered_html,
                    fail_silently=True,  # Silent failure to avoid interrupting the flow
                )
        else:
            # If no budget exists, set a default start date or skip budget-related logic
            budget_start_date = None  # Or set a default value if needed

        # Save the expense if it passes the budget check or if no budget exists
        tbl_expense.objects.create(
            expensecategory=expensetype,
            user=user,
            expense_amount=expense_amount,
            expense_bill=request.FILES.get('file_bill'),
            expense_note=expense_note,
        )

        # --- Check if the User Stayed Within Budget & Award Score ---
        # Fetch all budgets of the user
        budgets = tbl_budget.objects.filter(user=user)

        budget_exceeded = False  # Flag to check if any budget was exceeded
        for budget in budgets:
            budget_start = budget.date_added
            budget_end = budget_start + relativedelta(months=1)

            total_spent = tbl_expense.objects.filter(
                expensecategory=budget.expensecategory,
                user=user,
                expense_date__range=[budget_start, budget_end]
            ).aggregate(Sum('expense_amount'))['expense_amount__sum'] or 0

            if total_spent > float(budget.budget_amount):
                budget_exceeded = True
                break  # Stop checking if any budget was exceeded

        # If no budget exceeded and a budget exists, add a score for the period
        # if not budget_exceeded and latest_budget:  # Only award score if a budget exists
        #     tbl_score.objects.create(
        #         score_id=f"{user.id}_{budget_start_date.strftime('%Y%m%d')}",  # Unique score ID per budget period
        #         user=user
        #    )

        return render(request, "User/Expense.html", {
            "msg": msg,
            "expenseData": expenseData,
            "expensetypeData": expensetypeData
        })

    return render(request, "User/Expense.html", {
        "expenseData": expenseData,
        "expensetypeData": expensetypeData
    })

def deleteExpense(request,iid):
    tbl_expense.objects.get(id=iid).delete()
    return redirect("User:expense")

def repayment(request):
    user=tbl_user.objects.get(id=request.session["uid"])
    repaymentData = tbl_repayment.objects.filter(user = user)
    if request.method == 'POST':
        tbl_repayment.objects.create(
            repayment_amount=request.POST.get('txt_amount'),
            repayment_name=request.POST.get('txt_name'),
            repayment_tenure = request.FILES.get('tenure_bill'),
            user = tbl_user.objects.get(id=request.session["uid"])
        )
        return render(request,"User/Repayment.html",{"msg":"Inserted Successfully"})
    else:
        return render(request,"User/Repayment.html",{"repaymentData":repaymentData})

def repaymentnotification(request):
    user=tbl_user.objects.get(id=request.session["uid"])
    repaymentnotificationData = tbl_repaymentnotification.objects.filter(user = user)
    if request.method == 'POST':
        tbl_repaymentnotification.objects.create(
            repaymentnotification_title=request.POST.get('txt_title'),
            repaymentnotification_description=request.POST.get('txt_description'),
            repaymentnotification_amount=request.POST.get('txt_amount'),
            repaymentnotification_paymentdate = request.POST.get('txt_paymentdate'),
            repaymentnotification_notificationdate=request.POST.get('txt_notificationdate'),
            user = tbl_user.objects.get(id=request.session["uid"])
        )
        return render(request,"User/Repaymentnotification.html",{"msg":"Inserted Successfully"})
    else:
        return render(request,"User/Repaymentnotification.html",{"repaymentnotificationData":repaymentnotificationData})

def deleteNotification(request,iid):
    tbl_repaymentnotification.objects.get(id=iid).delete()
    return redirect("User:repaymentnotification")

def feedback(request):
    user=tbl_user.objects.get(id=request.session["uid"])
    feedbackData = tbl_feedback.objects.filter(user = user)
    if request.method == 'POST':
        tbl_feedback.objects.create(
            feedback_content = request.POST.get('txt_feedback'),
            user = tbl_user.objects.get(id=request.session["uid"])
        )
        return render(request,"User/Feedback.html",{"msg":"Inserted Successfully"})
    else:
        return render(request,"User/Feedback.html",{"feedbackData":feedbackData})

def deleteFeedback(request,iid):
    tbl_feedback.objects.get(id=iid).delete()
    return redirect("User:feedback")

def logout(request):
      del request.session["uid"]
      return redirect('Guest:index')


def financial_reports(request):
    user_id = request.session.get("uid")
    start_date = request.GET.get('start_date', (datetime.today() - timedelta(days=30)).strftime('%Y-%m-%d'))
    end_date = request.GET.get('end_date', datetime.today().strftime('%Y-%m-%d'))

    # Convert dates for filtering
    start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
    end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')

    # 1. Income by Category (Pie Chart)
    income_by_category = tbl_income.objects.filter(
        user_id=user_id,
        income_date__range=[start_date, end_date]
    ).values('incomecategory__incometype_name').annotate(total=Sum('income_amount'))

    # 2. Expenses by Category (Pie Chart)
    expenses_by_category = tbl_expense.objects.filter(
        user_id=user_id,
        expense_date__range=[start_date, end_date]
    ).values('expensecategory__expensetype_name').annotate(total=Sum('expense_amount'))

    # 3. Monthly Income (Bar Chart)
    monthly_income = tbl_income.objects.filter(
        user_id=user_id
    ).extra({'month': "strftime('%%Y-%%m', income_date)"}).values('month').annotate(total=Sum('income_amount'))

    # 4. Monthly Expenses (Bar Chart)
    monthly_expenses = tbl_expense.objects.filter(
        user_id=user_id
    ).extra({'month': "strftime('%%Y-%%m', expense_date)"}).values('month').annotate(total=Sum('expense_amount'))

    # 5. Budget vs Actual (Bar Chart)
    actual_expenses = tbl_expense.objects.filter(
        user_id=user_id,
        expense_date__range=[start_date, end_date]
    ).values('expensecategory__expensetype_name').annotate(actual=Sum('expense_amount'))
    # print(actual_expenses)
    budget_data = tbl_budget.objects.filter(
        user_id=user_id
    ).values('expensecategory__expensetype_name', 'budget_amount')
    # print(budget_data)
    budget_vs_actual = []
    actual_dict = {item['expensecategory__expensetype_name']: item['actual'] for item in actual_expenses}
    for budget in budget_data:
        category = budget['expensecategory__expensetype_name']
        budget_vs_actual.append({
            'expensecategory__expensetype_name': category,
            'budget_amount': budget['budget_amount'],
            'actual': actual_dict.get(category, 0)
        })
    print(budget_vs_actual)
    # 6. Savings Progress (Line Chart)
    savings_progress = tbl_savingbody.objects.filter(
        savinghead__user_id=user_id
    ).extra({'month': "strftime('%%Y-%%m', savingbody_date)"}).values('month').annotate(total=Sum('savingbody_amount'))

    # 7. Repayment Status (Pie Chart)
    repayment_status = tbl_repayment.objects.filter(
        user_id=user_id,
        repayment_date__range=[start_date, end_date]
    ).values('repayment_name').annotate(total=Sum('repayment_amount'))

    # 8. Income vs Expense Trend (Line Chart)
    income_expense_trend = {
        'income': list(tbl_income.objects.filter(user_id=user_id).extra({'month': "strftime('%%Y-%%m', income_date)"})
                      .values('month').annotate(total=Sum('income_amount'))),
        'expense': list(tbl_expense.objects.filter(user_id=user_id).extra({'month': "strftime('%%Y-%%m', expense_date)"})
                       .values('month').annotate(total=Sum('expense_amount')))
    }

    # 9. Top 5 Expenses (Bar Chart)
    top_expenses = tbl_expense.objects.filter(
        user_id=user_id,
        expense_date__range=[start_date, end_date]
    ).values('expensecategory__expensetype_name').annotate(total=Sum('expense_amount')).order_by('-total')[:5]

    # 10. Savings Goal Progress
    savings_goals = tbl_savinghead.objects.filter(
        user_id=user_id
    ).annotate(
        total_saved=Sum('tbl_savingbody__savingbody_amount')
    ).values('savinghead_title', 'savinghead_goal', 'total_saved')
    # print(savings_goals)

    # 11. Transaction History (Tabular)
    transactions = tbl_expense.objects.filter(
        user_id=user_id,
        expense_date__range=[start_date, end_date]
    ).values('expense_date', 'expense_amount', 'expensecategory__expensetype_name')

    # 12. Monthly Budget Summary (Tabular) - Fixed version
    spent_expenses = tbl_expense.objects.filter(
        user_id=user_id,
        expense_date__range=[start_date, end_date]
    ).values('expensecategory__expensetype_name').annotate(spent=Sum('expense_amount'))

    budget_data = tbl_budget.objects.filter(
        user_id=user_id
    ).values('expensecategory__expensetype_name', 'budget_amount')

    monthly_budget = []
    spent_dict = {item['expensecategory__expensetype_name']: item['spent'] for item in spent_expenses}
    for budget in budget_data:
        category = budget['expensecategory__expensetype_name']
        monthly_budget.append({
            'expensecategory__expensetype_name': category,
            'budget_amount': budget['budget_amount'],
            'spent': spent_dict.get(category, 0)
        })

    # 13. Complaint Status (Pie Chart)
    complaint_status = tbl_complaint.objects.filter(
        user_id=user_id
    ).values('complaint_status').annotate(count=Count('id'))

    # 14. Feedback Summary (Tabular)
    feedback_summary = tbl_feedback.objects.filter(
        user_id=user_id,
        feedback_date__range=[start_date, end_date]
    ).values('feedback_date', 'feedback_content')

    # 15. Notification History (Tabular)
    notifications = tbl_repaymentnotification.objects.filter(
        user_id=user_id,
        repaymentnotification_paymentdate__range=[start_date, end_date]
    ).values('repaymentnotification_title', 'repaymentnotification_paymentdate', 'last_acknowledged_date')

    context = {
        'start_date': start_date,
        'end_date': end_date,
        'income_by_category': json.dumps(list(income_by_category)),
        'expenses_by_category': json.dumps(list(expenses_by_category)),
        'monthly_income': json.dumps(list(monthly_income)),
        'monthly_expenses': json.dumps(list(monthly_expenses)),
        'budget_vs_actual': json.dumps(budget_vs_actual),
        'savings_progress': json.dumps(list(savings_progress)),
        'repayment_status': json.dumps(list(repayment_status)),
        'income_expense_trend': json.dumps(income_expense_trend),
        'top_expenses': json.dumps(list(top_expenses)),
        'savings_goals': json.dumps(list(savings_goals)),
        'transactions': list(transactions),
        'monthly_budget': list(monthly_budget),
        'complaint_status': json.dumps(list(complaint_status)),
        'feedback_summary': list(feedback_summary),
        'notifications': list(notifications),
    }

    return render(request, 'User/FinancialReports.html', context)