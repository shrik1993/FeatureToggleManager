"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest
from django.conf import settings
from django.contrib.auth.decorators import login_required
import pandas as pd


@login_required
def home(request):
    ex_data = pd.read_excel(settings.FEATURE_TOGGLE_FILE, skiprows=2)
    result = ex_data.to_json(orient='table')
    print(result)
    return render(
        request,
        'app/excel_data.html',
        {
            'ex_data': result,
        }
        
    )


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
