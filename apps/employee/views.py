import json
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.urls import reverse
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.utils.html import escape
from django.db.models import Q
from apps.employee.models import EmployeeDetails, EmployeeSettings
from apps.users.models import Users
from veuz_core.helpers.helper import get_object_or_none
from veuz_core.helpers.signer import URLEncryptionDecryption
from django.contrib import messages
from django.http import JsonResponse
from uuid import uuid4
# Create your views here.

class EmployeeManagementView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = {"breadcrumbs" : []}
        self.template = 'admin/home-page/employee-management/employee-list.html'
        self.context['title'] = 'Employee Management'
        self.generateBreadcrumbs()
        
        
    def get(self, request, *args, **kwargs):
        return render(request, self.template, context=self.context)

    def generateBreadcrumbs(self):
        self.context['breadcrumbs'].append({"name" : "Home", "route" : reverse('home:dashboard'), 'active' : False})
        self.context['breadcrumbs'].append({"name" : "Employee Management", "route" : '','active' : True})
        


class LoadEmployeeManagementDatatable(BaseDatatableView):
    model = EmployeeDetails
    order_columns = ['id']
    
    def get_initial_queryset(self):

        user_instance = get_object_or_none(Users, pk=self.request.user.id)

        # Build initial filter based on user permissions
        if not user_instance.is_superuser:
            base_filter = Q(created_by=user_instance)
        else:
            base_filter = Q()

        filter_value = self.request.POST.get('columns[3][search][value]', None)

        if filter_value == '1':
            additional_filter = Q(is_active=True)
        elif filter_value == '2':
            additional_filter = Q(is_active=False)
        elif filter_value == '3':
            additional_filter = Q() 
        else:
            additional_filter = Q()

        combined_filter = base_filter & additional_filter

        queryset = self.model.objects.filter(combined_filter).order_by('-id')
        return queryset
    
    def filter_queryset(self, qs):
        search = self.request.POST.get('search[value]', None)
        if search:
            qs = qs.filter(Q(name__istartswith=search) | Q(email__istartswith=search) | Q(phonenumber__istartswith=search))
        return qs

    
    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            json_data.append({
                'id'              : escape(item.id),
                'name'            : escape(item.name),
                'email'           : escape(item.email),
                'phonenumber'   : escape(item.phonenumber),
                'created_date'    : escape(item.created_date.strftime("%d-%m-%Y")),
                'is_active'       : escape(item.is_active),
                'encrypt_id'      : escape(URLEncryptionDecryption.enc(item.id)),
            })
        return json_data

class EmployeeManagementCreateOrUpdateView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.context = {"breadcrumbs": []}
        self.context['title'] = 'Employee Management'
        self.action = "Create"
        self.template = 'admin/home-page/employee-management/create-or-update-employee.html'

    def get(self, request, *args, **kwargs):
        id = URLEncryptionDecryption.dec(kwargs.pop('id', None))
        self.context['uuid'] = uuid4()
        if id:
            self.action = "Update"
            self.context['employee_management_obj'] = get_object_or_404(EmployeeDetails, id=id)
        self.generateBreadcrumbs()
        return render(request, self.template, context=self.context)

    def generateBreadcrumbs(self):
        self.context['breadcrumbs'].append({"name": "Home", "route": reverse('home:dashboard'), 'active': False})
        self.context['breadcrumbs'].append(
            {"name": "Employee Management", "route": reverse('employee:employee_management.index'), 'active': False})
        self.context['breadcrumbs'].append({"name": "{} Employee Management".format(self.action), "route": '', 'active': True})

    def post(self, request, *args, **kwargs):
        employee_management_id    = request.POST.get('employee_management_id', None)
        print("9999999999999999999999999999999999")
        try:
            if employee_management_id:
                self.action = 'Updated'
                employee_management_obj              = get_object_or_404(EmployeeDetails, id=employee_management_id)
                employee_management_obj.modified_by_id  = request.user.id
            else:
                self.action = 'Created'
                employee_management_obj         = EmployeeDetails()
            employee_management_obj.name        = request.POST.get('name')
            employee_management_obj.email       = request.POST.get('email')
            employee_management_obj.phonenumber = request.POST.get('phonenumber')
            employee_management_obj.created_by_id  = request.user.id
            employee_management_obj.save()
            
            messages.success(request, f"Data Successfully "+ self.action)
            
        except Exception as e:
            messages.error(request, f"Something went wrong."+str(e))
            if employee_management_id is not None:
                return redirect('employee:employee_management.update', id=URLEncryptionDecryption.dec(int(employee_management_id)))
            return redirect('employee:employee_management.create')
        return redirect('employee:employee_management.index')


class DestroyEmployeeManagementRecordsView(View):
    def __init__(self, **kwargs):
        self.response_format = {"status_code": 101, "message": "", "error": ""}

    def post(self, request, *args, **kwargs):
        try:
            employee_management_id = request.POST.getlist('ids[]')
            if employee_management_id:
                EmployeeDetails.objects.filter(id__in=employee_management_id).delete()
                self.response_format['status_code'] = 200
                self.response_format['message'] = 'Deleted successfully'
        except Exception as e:
            self.response_format['message'] = 'error'
            self.response_format['error'] = str(e)
            
        return JsonResponse(self.response_format, status=200)
    
    
class EmployeeManagementStatusChange(View):
    def __init__(self, **kwargs):
        self.response_format = {"status_code":101, "message":"", "error":""}
        
    def post(self, request, **kwargs):
        try:
            instance_id = request.POST.get('id', None)
            instance    = EmployeeDetails.objects.get(id = instance_id)
            if instance_id:
                if instance.is_active:
                    instance.is_active = False
                else:
                    instance.is_active =True
                instance.save()
                self.response_format['status_code']=200
                self.response_format['message']= 'Success'
                
        except Exception as es:
            self.response_format['message']='error'
            self.response_format['error'] = str(es)
        return JsonResponse(self.response_format, status=200)
    

class SettingsManagementCreateOrUpdateView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.context = {"breadcrumbs": []}
        self.context['title'] = 'Employee Settings'
        self.action = "Create"
        self.template = 'admin/home-page/employee-settings/create-or-update-employee-settings.html'

    def get(self, request, *args, **kwargs):
        id = URLEncryptionDecryption.dec(kwargs.pop('id', None))
        print("111111111111111111111111111", id)
        # import pdb;pdb.set_trace()
        self.context['uuid'] = uuid4()
        if id:
            self.action = "Update"
            self.context['employee_management_obj'] = get_object_or_404(EmployeeDetails, id=id)
            self.context['employee_settings_obj']   = EmployeeSettings.objects.filter(employee_details_id=id)

        self.generateBreadcrumbs()
        return render(request, self.template, context=self.context)

    def generateBreadcrumbs(self):
        self.context['breadcrumbs'].append({"name": "Home", "route": reverse('home:dashboard'), 'active': False})
        self.context['breadcrumbs'].append(
            {"name": "Employee Settings", "route": reverse('employee:employee_management.index'), 'active': False})
        self.context['breadcrumbs'].append({"name": "{} Employee Settings".format(self.action), "route": '', 'active': True})

    def post(self, request, *args, **kwargs):
        try:
            employee_management_id    = request.POST.get('employee_management_id', None)
            repeater_data = json.loads(request.POST.get('repeater_data', '[]'))
            EmployeeSettings.objects.filter(employee_details_id=employee_management_id).delete()
            print("111111111111111110", repeater_data)
            for repeater in repeater_data:
                employee_settings_obj = EmployeeSettings()

                employee_settings_obj.name  = repeater['name']
                employee_settings_obj.field_type  = repeater['type']
                employee_settings_obj.value  = repeater['value']
                employee_settings_obj.employee_details_id  = employee_management_id
                employee_settings_obj.created_by_id  = request.user.id
                employee_settings_obj.modified_by_id  = request.user.id
                employee_settings_obj.save()                                                                                                                    
            
            messages.success(request, f"Data Successfully "+ self.action)
            
        except Exception as e:
            messages.error(request, f"Something went wrong."+str(e))
            if employee_management_id is not None:
                return redirect('employee:employee_settings_management.update', id=URLEncryptionDecryption.dec(int(employee_management_id)))
            return redirect('employee:employee_settings_management.create')
        return redirect('employee:employee_management.index')