from django.contrib import admin
from .functions import mark_payed, mark_unpayed, e_mail, activate, inactivate

from .models import User, Attachment
from Enhance.admin import admin_site


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_active', 'paid')

    admin_site.add_action(mark_payed, 'Mark Paid')
    admin_site.add_action(mark_unpayed, 'Mark Not Paid')
    admin_site.add_action(activate, 'Make Active')
    admin_site.add_action(inactivate, 'Make InActive')
    admin_site.add_action(e_mail, 'Send Email')


admin_site.register(User, UserAdmin)


