from django.shortcuts import render
from django.http.response import HttpResponse
from report.gen_report_data import get_report_data

# Create your views here.
def view_report(request):
    report_map = get_report_data()
    return render(request, 'report.html', report_map)
