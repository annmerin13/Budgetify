from django.urls import path,include
from Admin import views
app_name="Admin"
urlpatterns = [
    path('incometype/',views.incometype,name="incometype"),
    path('deleteIncomeType/<int:iid>',views.deleteIncomeType,name="deleteIncomeType"),

    path('expensetype/',views.expensetype,name="expensetype"),
    path('deleteExpenseType/<int:iid>',views.deleteExpenseType,name="deleteExpenseType"),
    
    path('adminregistration/',views.adminregistration,name="adminregistration"),
    path('deleteAdmin/<int:iid>',views.deleteAdmin,name="deleteAdmin"),

    path('viewcomplaint/',views.viewcomplaint,name="viewcomplaint"),
    path('reply/<int:cid>',views.reply,name="reply"),
    path('homepage/',views.homepage,name="homepage"),
    path('logout/',views.logout,name="logout"),
    path('feedback/', views.feedback, name='feedback'),
]
