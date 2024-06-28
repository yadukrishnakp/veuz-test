import logging
from apps.employee.models import EmployeeDetails
from django.shortcuts import render
from django.views import View
logger = logging.getLogger(__name__)


class HomeView(View):
    def __init__(self):
        self.context = {}
        self.context['title'] = 'Dashboard'

    def get(self, request, *args, **kwargs):
        
        if request.user.is_superuser:
            user_queryset = EmployeeDetails.objects.all().count()
        else:
            user_queryset = EmployeeDetails.objects.filter(created_by_id=request.user.id).count()

        self.context['total_employees'] = user_queryset
        return render(request, "admin/home/dashboard.html", self.context)

