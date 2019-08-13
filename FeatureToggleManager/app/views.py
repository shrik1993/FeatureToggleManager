"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest
from django.conf import settings
from django.contrib.auth.decorators import login_required
import pandas as pd
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
import os
from app.common.utils import upload_file_to_dir, excel_to_json, get_datatable_data, excel_read, dict_to_dataframe, excel_append, excel_remove, get_latest_file_from_dir
import json

@login_required
def fileupload(request):
    print(request.FILES.get('infile'))
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

@login_required
def table_edit(request, table_name=""):
    if request.method == "GET":
        print(table_name)
        if table_name:
            return render(request, 'app/WebPage1.html',{"tb_name": "table found"})
        else:
            return render(request, 'app/WebPage1.html',{"tb_name": "tb_name not found."})
    if request.method == "POST":
        #try:
        req_data = {}
        for k, v in request.POST.items():
            req_data[k] = v
        print(req_data, table_name)
        file_dir = os.path.join(settings.MEDIA_ROOT, str(request.user))
        latest_file = get_latest_file_from_dir(file_dir)
        if request.user.is_superuser:
            ex_data = excel_read(latest_file)
        else:
            ex_data = excel_read(latest_file, skiprows=0)
        df = dict_to_dataframe(req_data)
        excel_append(ex_data, df, latest_file)
        return HttpResponse("Record added successfully.")
        #except:
        #    return HttpResponse("Fail to add record.")


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
