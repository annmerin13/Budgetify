from django.db import models
from Admin.models import *
from Guest.models import *

class tbl_complaint(models.Model):
    complaint_title = models.CharField(max_length=100)
    complaint_content = models.TextField(max_length=100)
    complaint_reply = models.TextField(max_length=100)
    complaint_date = models.DateField(auto_now_add=True)
    complaint_status = models.TextField(max_length=100)
    user = models.ForeignKey(tbl_user, on_delete=models.CASCADE)

class tbl_savinghead(models.Model):
    savinghead_title = models.CharField(max_length=30)
    savinghead_goal = models.TextField(max_length=100)
    savinghead_date = models.DateField(auto_now_add=True)
    user = models.ForeignKey(tbl_user, on_delete=models.CASCADE)

class tbl_budget(models.Model):
    budget_amount = models.FloatField()  # Changed to FloatField
    user = models.ForeignKey(tbl_user, on_delete=models.CASCADE)
    expensecategory = models.ForeignKey(tbl_expensetype, on_delete=models.CASCADE)
    date_added = models.DateField(auto_now_add=True)

class tbl_savingbody(models.Model):
    savingbody_amount = models.FloatField()  # Changed to FloatField
    savingbody_date = models.DateField(auto_now_add=True)
    savinghead = models.ForeignKey(tbl_savinghead, on_delete=models.CASCADE)
    

class tbl_income(models.Model):
    income_amount = models.FloatField()  # Changed to FloatField
    income_date = models.DateField(auto_now_add=True)
    income_note = models.TextField(max_length=30, blank=True)
    incomecategory = models.ForeignKey(tbl_incometype, on_delete=models.CASCADE)
    user = models.ForeignKey(tbl_user, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('User:edit_income', kwargs={'pk': self.pk})

class tbl_expense(models.Model):
    expense_amount = models.FloatField()  # Changed to FloatField
    expense_date = models.DateField(auto_now_add=True)
    expense_time = models.TimeField(auto_now_add=True)
    expense_note = models.TextField(max_length=30)
    expense_bill = models.FileField(upload_to='Assets/ExpenseBill/', blank=True, null=True)
    expensecategory = models.ForeignKey(tbl_expensetype, on_delete=models.CASCADE)
    user = models.ForeignKey(tbl_user, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('User:edit_expense', kwargs={'pk': self.pk})



class tbl_repayment(models.Model):
    repayment_amount = models.CharField(max_length=30)
    repayment_date = models.DateField(auto_now_add=True)
    repayment_tenure = models.FileField(upload_to='Assets/TenureBill/')
    repayment_name = models.TextField(max_length=30)
    user = models.ForeignKey(tbl_user, on_delete=models.CASCADE)

# class tbl_score(models.Model):
#     score_id = models.CharField(max_length=30)
#     score_date = models.DateField()
#     user = models.ForeignKey(tbl_user, on_delete=models.CASCADE)

class tbl_feedback(models.Model):
    feedback_date = models.DateField(auto_now_add=True)
    feedback_content = models.TextField(max_length=30)
    user = models.ForeignKey(tbl_user, on_delete=models.CASCADE)

class tbl_repaymentnotification(models.Model):
    repaymentnotification_title = models.TextField(max_length=30)
    repaymentnotification_description = models.TextField(max_length=100)
    repaymentnotification_amount = models.TextField(max_length=30)
    repaymentnotification_notificationdate = models.IntegerField()
    repaymentnotification_paymentdate = models.TextField(max_length=30)
    repaymentnotification_status = models.TextField(max_length=30)
    user = models.ForeignKey(tbl_user, on_delete=models.CASCADE)
    last_acknowledged_date = models.DateField(null=True, blank=True)  # New field
