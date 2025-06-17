from django.urls import path,include
from User import views
app_name="User"
urlpatterns = [
    # path('incometype/',views.incometype,name="incometype"),
    # path('deleteIncomeType/<int:iid>',views.deleteIncomeType,name="deleteIncomeType"),
    path('homepage/',views.homepage,name="homepage"),
    #path('userincome/',views.userincome,name="userincome"),
    #path('userexpense/',views.userexpense,name="userexpense"),
    path('complaint/',views.complaint,name="complaint"),
    path('reply/<int:cid>',views.reply,name="reply"),
    path('savinghead/',views.savinghead,name="savinghead"),
    path('budget/',views.budget,name="budget"),
    path('savingbody/<int:id>',views.savingbody,name="savingbody"),
    path('income/',views.income,name="income"),
    path('expense/',views.expense,name="expense"),
    path('repayment/',views.repayment,name="repayment"),
    path('feedback/',views.feedback,name="feedback"),
    path('myprofile/',views.myprofile,name="myprofile"),
    path('editprofile/',views.editprofile,name="editprofile"),
    path('repaymentnotification/',views.repaymentnotification,name="repaymentnotification"),
    path('logout/',views.logout,name="logout"),


    path('deleteComplaint/<int:iid>',views.deleteComplaint,name="deleteComplaint"),
    path('deleteSavingHead/<int:iid>',views.deleteSavingHead,name="deleteSavingHead"),
    path('deleteBudget/<int:iid>',views.deleteBudget,name="deleteBudget"),
    path('deleteIncome/<int:iid>',views.deleteIncome,name="deleteIncome"),
    path('deleteExpense/<int:iid>',views.deleteExpense,name="deleteExpense"),
    path('deleteFeedback/<int:iid>',views.deleteFeedback,name="deleteFeedback"),
    path('deleteNotification/<int:iid>',views.deleteNotification,name="deleteNotification"),


    path('reports/', views.financial_reports, name='financial_reports'),

    path('acknowledge-notification/', views.acknowledge_notification, name='acknowledge_notification'),

]
