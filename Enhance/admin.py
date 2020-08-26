from django.contrib.admin import AdminSite
from django.template.response import TemplateResponse
from django.views.decorators.cache import never_cache
from Account.functions import created_24hrs_ago, created_last_month, created_last_week, created_last_year


class EnhanceAdminSite(AdminSite):
    @never_cache
    def index(self, request, extra_context=None):
        """
                Display the main admin index page, which lists all of the installed
                apps that have been registered in this site.
                """
        app_list = self.get_app_list(request)

        context = {
            **self.each_context(request),
            'title': self.index_title,
            'app_list': app_list,
            **(extra_context or {}),
            'last_day': created_24hrs_ago(),
            'last_week': created_last_week(),
            'last_month': created_last_month(),
            'last_year': created_last_year()
        }

        request.current_app = self.name

        return TemplateResponse(request, self.index_template or 'admin/index.html', context)


admin_site = EnhanceAdminSite()