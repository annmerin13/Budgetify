from django.shortcuts import render,redirect
from .models import *
from User.models import *
# Create your views here.
def incometype(request):
    incometypeData = tbl_incometype.objects.all()
    if request.method=="POST":
        tbl_incometype.objects.create(incometype_name=request.POST.get("txt_incometype"))
        return render(request,"Admin/Incometype.html",{"msg":"Inserted Successfully"})
    else:
        return render(request,"Admin/Incometype.html",{"incometypeData":incometypeData})


def deleteIncomeType(request,iid):
    tbl_incometype.objects.get(id=iid).delete()
    return redirect("Admin:incometype")

def deleteExpenseType(request,iid):
    tbl_expensetype.objects.get(id=iid).delete()
    return redirect("Admin:expensetype")

def deleteAdmin(request,iid):
    tbl_adminregistration.objects.get(id=iid).delete()
    return redirect("Admin:adminregistration")

def expensetype(request):
    expensetypeData = tbl_expensetype.objects.all()
    if request.method=="POST":
        tbl_expensetype.objects.create(expensetype_name=request.POST.get("txt_expensetype"))
        return render(request,"Admin/Expensetype.html",{"msg":"Inserted Successfully"})
    else:
        return render(request,"Admin/Expensetype.html",{"expensetypeData":expensetypeData})

def adminregistration(request):
    adminData = tbl_adminregistration.objects.all()
    if request.method=="POST":
        tbl_adminregistration.objects.create(admin_name=request.POST.get("txt_name"),admin_email=request.POST.get("txt_email"),admin_password=request.POST.get("txt_password"))
        return render(request,"Admin/Adminregistration.html",{"msg":"Inserted Successfully"})
    else:
        return render(request,"Admin/Adminregistration.html",{"adminData":adminData})
    
def logout(request):
      del request.session["aid"]
      return redirect('Guest:index')


def viewcomplaint(request):
    complaintData = tbl_complaint.objects.all()

    return render(request,"Admin/Viewcomplaint.html",{"complaintData":complaintData})

def reply(request,cid):
    if request.method=="POST":
        complaintData = tbl_complaint.objects.get(id=cid)
        replyData = request.POST.get("txt_reply")
        complaintData.complaint_reply=replyData
        complaintData.save()
        return redirect("Admin:viewcomplaint")
    else:
        return render(request,"Admin/Reply.html")

def feedback(request):
    feedback_data = tbl_feedback.objects.all()  # Fetch all feedback entries
    return render(request, "Admin/Feedback.html", {'feedbackData': feedback_data})


def homepage(request):
    return render(request,"Admin/HomePage.html")
