from django.apps import AppConfig
from django.contrib.admin.apps import AdminConfig


class AccountConfig(AppConfig):
    name = 'Account'


class EnhanceAdminConfig(AdminConfig):
    default_site = 'Enhance.admin.EnhanceAdminSite'
