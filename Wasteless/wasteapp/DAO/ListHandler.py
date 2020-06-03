from django.utils import timezone
from wasteapp.models import User, GList, Item

class ListHandler:
    def getListByName(self, user, list_name):
        return user.glist_set.get(name=list_name)

    def addList(self, user, list_name):
        user.glist_set.create(name=list_name, date=timezone.now())

    def delete(self, o):
        o.delete()

    def getSpecificList(self, user, list_name):
        return user.glist_set.filter(name=list_name)

    def getItemsOfList(self, lst):
        return lst.item_set.all()