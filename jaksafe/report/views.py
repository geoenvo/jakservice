#from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

'''
def index(request):
    return HttpResponse("Hello world!")
'''

def index(request, template='report/index.html'):
    context_dict = {}
    context_dict["page_title"] = 'Report'
    return render_to_response(template, RequestContext(request, context_dict))