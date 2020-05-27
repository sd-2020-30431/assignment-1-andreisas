from django.utils import timezone
from .models import User, GList, Item
class dbh:

    def getUserByName(name):
        return User.objects.get(name = name)

    def userFound(name):
        try:
            User.objects.filter(name = name)[0]
        except IndexError:
            return False
        return True

    def getListsOfUser(user):
        return user.glist_set.all()


    def getItemsOfList(lst):
        return lst.item_set.all()

    def deleteDBObject(o):
        o.delete()

    def getSpecificList(user, list_name):
        return user.glist_set.filter(name=list_name)

    def getListByName(user, list_name):
        return user.glist_set.get(name=list_name)

    def addList(user, list_name):
        user.glist_set.create(name=list_name, date=timezone.now())
    
    def addItem(lst, name, cals, exp_date):
        lst.item_set.create(name=name, cals=cals, exp_date=exp_date)

    def addUser(name, password, cals):
        new_user = User(name = name, password = password, cals = cals)
        new_user.save()

