from django.shortcuts import render
from django.utils import timezone
from datetime import date
from datetime import datetime

from .models import User, GList, Item

def index(request, context=dict()):
    return render(request, 'wasteapp/index.html', context)

def login(request):
    name = request.POST['name']
    pw = request.POST['pw']
    user = User.objects.get(name = name)
    if user and pw == user.password:
        lists = GList.objects.filter(user = user.id)
        edible, soon_expire, expired = getStats(user)
        context = {'lists':lists, 'user':user, 'edible':edible, 'soon_expire':soon_expire, 'expired':expired}
        return render(request, "wasteapp/myaccount.html", context)
    else:
        return render(request, "wasteapp/index.html", {'context':"Name or password incorrect!"})


def addForm(request):
    name = request.POST['name']
    pw = request.POST['pw']
    context = {'user_name':name, 'user_pw':pw}
    return render(request, "wasteapp/addForm.html", context)


def getStats(user):
    lists = user.glist_set.all()
    edible_cals = 0
    expired_cals = 0
    soon_expire_cals = 0
    for li in lists:
        litems = li.item_set.all()
        for litem in litems:
            availability = (litem.exp_date - timezone.make_aware(datetime.now(), timezone.get_default_timezone())).days
            if availability > 2:
                edible_cals += litem.cals
            elif availability >0 and availability <= 2:
                soon_expire_cals += litem.cals
            else:
                expired_cals += litem.cals
    return edible_cals, soon_expire_cals, expired_cals

def removeItems(request):
    user = User.objects.get(name = request.POST['name'])
    lists = user.glist_set.all()
    if request.POST['action'] == "donate":
        for l in lists:
            items = l.item_set.all()
            for litem in items:
                if (litem.exp_date - timezone.make_aware(datetime.now(), timezone.get_default_timezone())).days <= 2 and (litem.exp_date - timezone.make_aware(datetime.now(), timezone.get_default_timezone())).days > 0:
                    litem.delete()
            try:
                l.item_set.all()[0]
            except IndexError:
                l.delete()
    else:
        for l in lists:
            items = l.item_set.all()
            for litem in items:
                if (litem.exp_date - timezone.make_aware(datetime.now(), timezone.get_default_timezone())).days <= 0:
                    litem.delete()
            try:
                l.item_set.all()[0]
            except IndexError:
                l.delete()
    lists = user.glist_set.all()
    edible, soon_expire, expired = getStats(user)
    context = {'lists':lists, 'user':user, 'edible':edible, 'soon_expire':soon_expire, 'expired':expired}

    return render(request, "wasteapp/myaccount.html", context)

def addNewList(request):
    user_name = request.POST['name']
    user_pw = request.POST['pw']
    list_name = request.POST['list_name']
    user = User.objects.get(name=user_name)
    user.glist_set.create(name=list_name, date=timezone.now())
    new_list = user.glist_set.get(name=list_name)
    i = 0
    
    while ('name_' + str(i)) in request.POST.keys():
        new_list.item_set.create(name = request.POST['name_' + str(i)], cals = request.POST['cals_' + str(i)], exp_date = datetime.fromisoformat(request.POST['date_' + str(i)]))
        i+=1
    lists = user.glist_set.all()
    edible, soon_expire, expired = getStats(user)
    context = {'lists':lists, 'user':user, 'edible':edible, 'soon_expire':soon_expire, 'expired':expired}
    return render(request, "wasteapp/myaccount.html", context)

