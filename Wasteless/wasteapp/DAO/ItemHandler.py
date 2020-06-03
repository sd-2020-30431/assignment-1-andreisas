from django.utils import timezone
from wasteapp.models import User, GList, Item

class ItemHandler:
    def addItem(self, lst, name, cals, exp_date):
        lst.item_set.create(name=name, cals=cals, exp_date=exp_date)

    def delete(self, o):
        o.delete()
