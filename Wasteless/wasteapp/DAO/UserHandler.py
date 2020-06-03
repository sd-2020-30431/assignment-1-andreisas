from django.utils import timezone
from wasteapp.models import User, GList, Item

class UserHandler:
    def getUserByName(self, name):
        return User.objects.get(name = name)

    def userFound(self, name):
        try:
            User.objects.filter(name = name)[0]
        except IndexError:
            return False
        return True

    def getListsOfUser(self, user):
        return user.glist_set.all()

    def delete(self, o):
        o.delete()

    def addUser(self, name, password, cals):
        new_user = User(name = name, password = password, cals = cals)
        new_user.save()
