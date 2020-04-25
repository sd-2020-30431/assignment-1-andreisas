from django.contrib import admin

from .models import User, GList, Item


class ListInline(admin.TabularInline):
    model = GList
    extra = 3



class UserAdmin(admin.ModelAdmin):
    fieldsets = [(None, {'fields': ['name']}),]
    inlines = [ListInline]

admin.site.register(User, UserAdmin)
