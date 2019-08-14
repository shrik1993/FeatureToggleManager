#!c:/Python/python.exe
from django.conf import settings
import os
from django.core.files.storage import FileSystemStorage
import pandas as pd
import json
import glob

def upload_file_to_dir(user, uploaded_file):
    """
    Upload file to media root with base directory of the user
    :return local machine file path, url for uploaded file.
    """
    file_dir = os.path.join(settings.MEDIA_ROOT, str(user))
    fs = FileSystemStorage(location=file_dir)
    filename = fs.save(str(user)+".xlsx", uploaded_file)
    uploaded_file_url = fs.url(file_dir+"/"+filename)
    uploaded_file_path = file_dir+"/"+filename
    return uploaded_file_path, uploaded_file_url

def excel_to_json(filepath, skip_rows=2):
    """
    Converts excelsheet data to json data.
    :return  JSON data
    """
    ex_data = pd.read_excel(filepath, skiprows=skip_rows)
    result = ex_data.to_json(orient='table')
    return result

def get_datatable_data(json_data, table_name='admin_table'):
    """
    Get the required data from the converted excelsheet data.
    :return reuired data
    """

    data = json.loads(json_data)
    return {'data': data['data']}

def get_latest_file_from_dir(dir):
    """
    Get the latest file created file form the given directory.
    """
    list_of_files = glob.glob(dir+'/*') # * means all if need specific format then *.csv
    latest_file = max(list_of_files, key=os.path.getctime)
    return latest_file

def excel_read(file_path, skiprows=2):
    """
    Read excel file and get the dataframes.
    """
    ex_data = pd.read_excel(file_path, skiprows=skiprows, index_col=False)
    return ex_data

def dict_to_dataframe(in_dict):
    df  = pd.DataFrame([in_dict], columns=in_dict.keys())
    return df

def excel_append(ex_data, append_dataframe, filepath):
    try:
        print("IN append before: {0}".format(ex_data))
        ex_data = pd.concat([ex_data, append_dataframe], axis=0, ignore_index=True, sort=False)
        print("IN append after: {0}".format(ex_data))
        ex_data.to_excel(filepath, index=False)
    except:
        raise Exception('Excel append record failed.')

def excel_remove(ex_data, drop_index, filepath):
    try:
        print("IN delete before: {0}".format(ex_data))
        new_ex_data = ex_data.drop(drop_index, axis=0)
        print("IN delete after: {0}".format(new_ex_data))
        new_ex_data.to_excel(filepath, index=False)
    except:
        raise Exception('Excel remove record failed.')
        
def read_user_excel(user, is_superuser):
    """
    Reads excel as per the skipped rows for admin and team.
    """

    file_dir = os.path.join(settings.MEDIA_ROOT, str(user))
    latest_file = get_latest_file_from_dir(file_dir)
    if not latest_file:
        latest_file = "{0}/{1}.{2}".format(file_dir, user, ".xlsx")
    if is_superuser:
        ex_data = excel_read(latest_file)
    else:
        ex_data = excel_read(latest_file, skiprows=0)
    return ex_data, latest_file

def excel_update(ex_data, update_dataframe, filepath):
    """
    Update existing record in the excel file.
    """
    try:
        print("IN update before: {0}".format(ex_data))
        ex_data.update(update_dataframe)
        ex_data.to_excel(filepath, index=False)
        print("IN update after: {0}".format(ex_data))
    except:
        raise Exception('Excel update record failed.')
