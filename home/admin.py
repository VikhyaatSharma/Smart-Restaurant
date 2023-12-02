from django.contrib import admin
from home.models import Tokens
from home.models import Menu
from home.models import Current_Orders
from home.models import Completed_Orders


# Register your models here.
admin.site.register(Tokens)
admin.site.register(Menu)
admin.site.register(Current_Orders)
admin.site.register(Completed_Orders)