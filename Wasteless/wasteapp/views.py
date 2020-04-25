from django.shortcuts import render
from django.utils import timezone
from datetime import date

from .models import User, GList, Item

def index(request, context=dict()):
    return render(request, 'wasteapp/index.html', context)

def login(request):
    name = request.POST['name']
    pw = request.POST['pw']
    user = User.objects.get(name = name)
    if user and pw == user.password:
        lists = GList.objects.filter(user = user.id)
        context = {'lists':lists, 'user_id':user.id, 'user_name':user.name, 'user_pw':user.password}
        return render(request, "wasteapp/myaccount.html", context)
    else:
        return render(request, "wasteapp/index.html", {'context':"Name or password incorrect!"})


def addForm(request):
    name = request.POST['name']
    pw = request.POST['pw']
    context = {'user_name':name, 'user_pw':pw}
    return render(request, "wasteapp/addForm.html", context)

def addNewList(request):
    user_name = request.POST['name']
    user_pw = request.POST['pw']
    list_name = request.POST['list_name']
    user = User.objects.get(name=user_name)
    user.glist_set.create(name=list_name, date=timezone.now())
    new_list = user.glist_set.get(name=list_name)
    i = 0
    
    while ('name_' + str(i)) in request.POST.keys():
        new_list.item_set.create(name = request.POST['name_' + str(i)], cals = request.POST['cals_' + str(i)], exp_date = date.fromisoformat(request.POST['date_' + str(i)]))
        i+=1
    
    return render(request, "wasteapp/index.html")

