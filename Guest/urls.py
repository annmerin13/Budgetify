from django.urls import path,include
from Guest import views
app_name="Guest"
urlpatterns = [
    # path('incometype/',views.incometype,name="incometype"),
    # path('deleteIncomeType/<int:iid>',views.deleteIncomeType,name="deleteIncomeType"),
    path('userregistration/',views.userregistration,name="userregistration"),
    path('Login/',views.Login,name="Login"),
    path('LoginAdmin',views.LoginAdmin,name="LoginAdmin"),
    path('',views.index,name="index"),
]
