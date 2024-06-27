import json
import logging
import uuid
from apps.employee.models import EmployeeDetails
from apps.home.functions import ConvertBase64File
from veuz_core import settings
from veuz_core.helpers.module_helper import imageDeletion
from django.contrib import messages
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.shortcuts import get_object_or_404, render,redirect
from django.views import View
from django.urls import reverse
from django.utils.html import escape
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from veuz_core.helpers.signer import URLEncryptionDecryption
import requests
from urllib.parse import urlparse
import os
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
logger = logging.getLogger(__name__)
from apps.users.models import Users


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

