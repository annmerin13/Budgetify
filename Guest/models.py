from django.db import models

# Create your models here.
class tbl_user(models.Model):
    user_name = models.CharField(max_length=30)
    user_email = models.CharField(max_length=30)
    user_password = models.CharField(max_length=30)

    def get_net_worth(self):
        income = self.tbl_income_set.all().aggregate(Sum('income_amount'))['income_amount__sum'] or 0
        expense = self.tbl_expense_set.all().aggregate(Sum('expense_amount'))['expense_amount__sum'] or 0
        savings = sum(head.tbl_savingbody_set.all().aggregate(Sum('savingbody_amount'))['savingbody_amount__sum'] or 0 
                   for head in self.tbl_savinghead_set.all())
        return income - expense + savings
    
    def get_monthly_summary(self, year, month):
        income = self.tbl_income_set.filter(
            income_date__year=year,
            income_date__month=month
        ).aggregate(Sum('income_amount'))['income_amount__sum'] or 0
        
        expense = self.tbl_expense_set.filter(
            expense_date__year=year,
            expense_date__month=month
        ).aggregate(Sum('expense_amount'))['expense_amount__sum'] or 0
        
        savings = sum(
            head.tbl_savingbody_set.filter(
                savingbody_date__year=year,
                savingbody_date__month=month
            ).aggregate(Sum('savingbody_amount'))['savingbody_amount__sum'] or 0
            for head in self.tbl_savinghead_set.all()
        )
        
        return {
            'income': income,
            'expense': expense,
            'savings': savings,
            'net': income - expense + savings
        }
