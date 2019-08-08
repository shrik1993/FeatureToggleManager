#!c:/Python/python.exe
from django.conf import settings
import os
from django.core.files.storage import FileSystemStorage
import pandas as pd
import json

def upload_file_to_dir(user, uploaded_file):
    file_dir = os.path.join(settings.MEDIA_ROOT, str(user))
    fs = FileSystemStorage(location=file_dir)
    filename = fs.save(str(user)+".xlsx", uploaded_file)
    uploaded_file_url = fs.url(file_dir+"/"+filename)
    uploaded_file_path = file_dir+"/"+filename
    return uploaded_file_path, uploaded_file_url

def excel_to_json(filepath, skip_rows=2):
    ex_data = pd.read_excel(filepath, skiprows=skip_rows)
    result = ex_data.to_json(orient='table')
    return result

def get_datatable_data(json_data, table_name='admin_table'):
    data = json.loads(json_data)
    return {'data': data['data']}
