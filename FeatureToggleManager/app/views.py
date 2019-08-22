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
from app.common.utils import upload_file_to_dir, excel_to_json, get_datatable_data, excel_read, dict_to_dataframe, excel_append, excel_remove, get_latest_file_from_dir, read_user_excel, excel_remove, excel_update, excel_data_to_teamwise_data, dataframe_to_mongodata, mongodata_to_dict, ex_data_to_mongo_data
import json
from django.views.generic import View
from django.http import QueryDict
from app.models import TeamData

@login_required
def fileupload(request):
    if request.method == 'POST' and request.FILES['infile']:
        file_dir = os.path.join(settings.MEDIA_ROOT, str(request.user))
        uploaded_file_path, uploaded_file_url = upload_file_to_dir(request.user, request.FILES['infile'])
        #result = excel_to_json(uploaded_file_path)
        #d_data = get_datatable_data(result)
        result, cols = ex_data_to_mongo_data(uploaded_file_path)
        teams_data = []
        for k, v in result.items():
            teams_data.append(TeamData(columns=cols, data=[list(val.values()) for val in v], team_name=k))
        TeamData.objects.bulk_create(teams_data)
        return render(request, 'app/excel_data.html', 
                      {'uploaded_file_url': uploaded_file_url,
                       'd_data': json.dumps(result),
                       'dashboard_title': "Admin Dashboard",
                       'year':datetime.now().year,
        })
    return render(request, 'app/excel_data.html', {'year':datetime.now().year})

@login_required
def home(request):
    result = {}
    dashboard_title = ""
    if not request.user.is_superuser:
        dashboard_title = "Team Dashboard"
    file_dir = os.path.join(settings.MEDIA_ROOT, str(request.user))
    #try:
    #latest_file = get_latest_file_from_dir(file_dir)
    #result = excel_data_to_teamwise_data(latest_file)
    #cols, data = dataframe_to_mongodata(latest_file)
    #teams_data = TeamData(columns=cols, data=data)
    #print('hi')
    #teams_data.save()
    data_dict={}
    #try:
    latest_record = TeamData.objects.values('team_name', 'columns', 'data')
    print(latest_record.values())
    #if latest_record:
        #data_dict = mongodata_to_dict(latest_record)
        #print(data_dict)
    #except:
        #pass
    return render(
        request,
        'app/excel_data.html',
        {
            'd_data': json.dumps(data_dict),
            'title':'Home',
            'dashboard_title': dashboard_title,
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
