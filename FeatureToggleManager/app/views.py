"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
import pandas as pd
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
import os
from app.common.utils import upload_file_to_dir, excel_to_json, get_datatable_data, excel_read, dict_to_dataframe, excel_append, excel_remove, get_latest_file_from_dir, read_user_excel, excel_remove, excel_update
import json
from django.views.generic import View
from django.http import QueryDict

@login_required
def fileupload(request):
    if request.method == 'POST' and request.FILES['infile']:
        file_dir = os.path.join(settings.MEDIA_ROOT, str(request.user))
        uploaded_file_path, uploaded_file_url = upload_file_to_dir(request.user, request.FILES['infile'])
        result = excel_to_json(uploaded_file_path)
        d_data = get_datatable_data(result)
        return render(request, 'app/excel_data.html', 
                      {'uploaded_file_url': uploaded_file_url,
                       'd_data': json.dumps(d_data),
                       'dashboard_title': "Admin Dashboard",
                       'year':datetime.now().year,
                       'test_data': d_data,
        })
    return render(request, 'app/excel_data.html', {'year':datetime.now().year})

@login_required
def home(request):
    return render(
        request,
        'app/excel_data.html',
        {
            'title':'Home',
            'message':'Dashboard.',
            'dashboard_title': "Dashboard",
            'year':datetime.now().year,
        }
    )

class EditTable(LoginRequiredMixin, View):
    http_method_names = ['post', 'put', 'delete']

    @method_decorator(login_required)
    def post(self, *args, **kwargs):
        try:
            req_data = {}
            for k, v in self.request.POST.items():
                req_data[k] = v
            tb_name = req_data.pop('table_name')
            ex_data, latest_file = read_user_excel(self.request.user, self.request.user.is_superuser)
            df = dict_to_dataframe(req_data)
            excel_append(ex_data, df, latest_file)
            return HttpResponse(json.dumps("Record added successfully."))
        except:
            raise Exception("Fail to add record.")

    @method_decorator(login_required)
    def put(self, *args, **kwargs):
        try:
            put = QueryDict(self.request.body)
            req_data = {}
            for k, v in put.items():
                req_data[k] = v
            tb_name = req_data.pop('table_name')
            ex_data, latest_file = read_user_excel(self.request.user, self.request.user.is_superuser)
            df = dict_to_dataframe(req_data)
            excel_update(ex_data, df, latest_file)
            return HttpResponse(json.dumps("Record added successfully."))
        except:
            raise Exception("Fail to add record.")

    @method_decorator(login_required)
    def delete(self, *args, **kwargs):
        try:
            delete_r = QueryDict(self.request.body)
            tb_name = delete_r.get('table_name')
            index_id = delete_r.get('index_id')
            ex_data, latest_file = read_user_excel(self.request.user, self.request.user.is_superuser)
            excel_remove(ex_data, int(index_id), latest_file)
            return HttpResponse(json.dumps("Record deleted successfully."))
        except: 
            raise Exception('Record delete failed.')


def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )
