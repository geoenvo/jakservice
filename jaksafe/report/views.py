from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

'''
def index(request):
    return HttpResponse("Hello world!")
'''

def report_auto(request, template='report/report_auto.html'):
    context_dict = {}
    context_dict["page_title"] = 'JakSAFE Automatic Report'
    
    if request.method == "POST":
        # handle form submit
        return HttpResponse("form submit")
    else:
        return render_to_response(template, RequestContext(request, context_dict))

def report_adhoc(request, template='report/report_adhoc.html'):
    context_dict = {}
    context_dict["page_title"] = 'JakSAFE Ad Hoc DaLA Report'
    
    if request.method == "POST":
        # handle form submit
        return HttpResponse("form submit")
    else:
        return render_to_response(template, RequestContext(request, context_dict))