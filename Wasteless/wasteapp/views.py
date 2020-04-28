from django.shortcuts import render
from django.utils import timezone
from datetime import date
from datetime import datetime
import re
from .models import User, GList, Item

def index(request, context=dict()):
    return render(request, 'wasteapp/index.html', context)

def login(request):
    name = request.POST['name']
    pw = request.POST['pw']
    context = {'message':""}
    if userFound(name):
        user = User.objects.get(name = name)
    else:
        context['message'] = "Username does not exist!"
        return render(request, "wasteapp/index.html", context)
    context = {'message':""}
    if pw == user.password:
        context['message'] = "Welcome back " + name + "!"
        return renderMyAccount(request, user, context['message'])
    else:
        context['message'] = "Wrong password!"
        return render(request, "wasteapp/index.html", context)


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

def renderMyAccount(request, user, message):
    lists = user.glist_set.all()
    edible, soon_expire, expired = getStats(user)
    context = {'lists':lists, 'user':user, 'edible':edible, 'soon_expire':soon_expire, 'expired':expired, 'message': message}
    return render(request, "wasteapp/myaccount.html", context)

def renderIndex(request, message):
    context = {'message': message}
    return render(request, "wasteapp/index.html", context)

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
        return renderMyAccount(request, user, "The items were donated")
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
        return renderMyAccount(request, user, "The expired items were thrown to the garbage")

def addNewList(request):
    user_name = request.POST['name']
    user_pw = request.POST['pw']
    list_name = request.POST['list_name']
    user = User.objects.get(name=user_name)
    if user.glist_set.filter(name=list_name):
        return renderMyAccount(request, user, "A list with the same name already exists")
        
    user.glist_set.create(name=list_name, date=timezone.now())
    new_list = user.glist_set.get(name=list_name)
    i = 0
    
    while ('name_' + str(i)) in request.POST.keys():
        new_list.item_set.create(name = request.POST['name_' + str(i)], cals = request.POST['cals_' + str(i)], exp_date = datetime.fromisoformat(request.POST['date_' + str(i)]))
        i+=1
    return renderMyAccount(request, user, "A new list was added")

def consumeItem(request):
    user = User.objects.get(name = request.POST['name'])
    lists = user.glist_set.all()
    for l in lists:
        items = l.item_set.all()
        for litem in items:
            if litem.name == request.POST['item_name']:
                litem.delete()
                try:
                    l.item_set.all()[0]
                except IndexError:
                    l.delete()
                return renderMyAccount(request, user, "Item consumed")
    return renderMyAccount(request, user, "Item not found")

def userFound(name):
    try:
       User.objects.filter(name = name)[0]
    except IndexError:
        return False
    return True

def match(t1, t2):
    if t1 == t2:
        return True
    return False

def passwordTemplate(passwd):
    SpecialSym =['$', '@', '#', '%', '!'] 
    if len(passwd) < 6: 
        print("Less than 6")
        return False
          
    if len(passwd) > 20: 
        print ("More than 20")
        return False
          
    if not any(char.isdigit() for char in passwd): 
        print("No digits")
        return False
          
    if not any(char.isupper() for char in passwd): 
        print("No upper")
        return False
          
    if not any(char.islower() for char in passwd): 
        print("No lower")
        return False
          
    if not any(char in SpecialSym for char in passwd): 
        print("No special")
        return False
    return True

def register(request):
    name = request.POST['name']
    pw1 = request.POST['pw1']
    pw2 = request.POST['pw2']
    cals = request.POST['cals']
    email = request.POST['email']
    context = {'message':""}
    if userFound(name):
        return renderIndex(request, "Username already in use.")
    elif not match(pw1, pw2):
        return renderIndex(request, "Passwords don't match.")
    elif not passwordTemplate(pw1):
        return renderIndex(request, "Password does not meet the requirements.")
    else:
        new_user = User(name = name, password = pw1, cals = cals)
        new_user.save()
        return renderMyAccount(request, new_user, "Welcome " + name + "!")


