from django.utils import timezone
from datetime import date
from datetime import datetime
from .models import User, GList, Item
from .dbHandler import dbh

class factoryReport:

    def getReport(ReportType, user):
        if ReportType == "week":
            text = "The items that will expire this week: "
            lists = dbh.getListsOfUser(user)
            for li in lists:
                litems = dbh.getItemsOfList(li)
                for litem in litems:
                    availability = (litem.exp_date - timezone.make_aware(datetime.now(), timezone.get_default_timezone())).days
                    if availability >0 and availability <= 7:
                        text += litem.name + " " 

        elif ReportType == "month":
            text = "The items that will expire this month: "
            lists = dbh.getListsOfUser(user)
            for li in lists:
                litems = dbh.getItemsOfList(li)
                for litem in litems:
                    availability = (litem.exp_date - timezone.make_aware(datetime.now(), timezone.get_default_timezone())).days
                    if availability >0 and availability <= 30:
                        text += litem.name + " "
        else:
            text = "Error getting the type of report"

        return text