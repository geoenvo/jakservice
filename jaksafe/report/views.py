from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.db import connection
from datetime import datetime

'''
def index(request):
    return HttpResponse("Hello world!")
'''

def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]

def valid_date(t0, t1):
    if (t0 != '' and t1 != ''):
        t0 += ' 00:00:00' # '2015-01-01 00:00:00'
        t1 += ' 23:59:59' # '2015-01-01 23:59:59'
        
        start = datetime.strptime(t0, '%Y-%m-%d %H:%M:%S')
        end = datetime.strptime(t1, '%Y-%m-%d %H:%M:%S')
        
        if (t0 > t1):
            return False
        
        return {'t0': start, 't1': end}
    
    return False
    
def report_auto(request, template='report/report_auto.html'):
    context_dict = {}
    context_dict["page_title"] = 'JakSAFE Automatic Report'
    
    cursor = connection.cursor()
    
    if request.method == "POST":
        # handle form submit
        t0 = request.POST.get('t0')
        t1 = request.POST.get('t1')
        
        date_range = valid_date(t0, t1)
        
        if (date_range != False):
            # process filter
            print "t0 = %s, t1 = %s" % (date_range['t0'], date_range['t1'])
            
            cursor.execute("SELECT id, t0, t1, damage, loss FROM auto_calc WHERE t0 >= '%s' AND t1 <= '%s' ORDER BY id DESC" % (date_range['t0'], date_range['t1']))
            
            resultset = dictfetchall(cursor)
            
            context_dict["date_range"] = date_range
            context_dict["auto_calc"] = resultset
        else:
            context_dict["error_invalid_date"] = True
    else:
        cursor.execute("SELECT id, t0, t1, damage, loss FROM auto_calc ORDER BY id DESC")
        
        resultset = dictfetchall(cursor)
        
        context_dict["auto_calc"] = resultset
        
    return render_to_response(template, RequestContext(request, context_dict))

def report_adhoc(request, template='report/report_adhoc.html'):
    context_dict = {}
    context_dict["page_title"] = 'JakSAFE Ad Hoc DaLA Report'
    
    cursor = connection.cursor()
    
    if request.method == "POST":
        # handle form submit
        t0 = request.POST.get('t0')
        t1 = request.POST.get('t1')
        
        date_range = valid_date(t0, t1)
        
        if (date_range != False):
            # process filter
            print "t0 = %s, t1 = %s" % (date_range['t0'], date_range['t1'])
            
            cursor.execute("SELECT id, t0, t1, damage, loss FROM adhoc_calc WHERE t0 >= '%s' AND t1 <= '%s' ORDER BY id DESC" % (date_range['t0'], date_range['t1']))
            
            resultset = dictfetchall(cursor)
            
            context_dict["date_range"] = date_range
            context_dict["adhoc_calc"] = resultset
        else:
            context_dict["error_invalid_date"] = True
    else:
        cursor.execute("SELECT id, t0, t1, damage, loss FROM adhoc_calc ORDER BY id DESC")
        
        resultset = dictfetchall(cursor)
        
        context_dict["adhoc_calc"] = resultset
        
    return render_to_response(template, RequestContext(request, context_dict))

def report_impact_config(request, template='report/report_impact_config.html'):
    context_dict = {}
    context_dict["page_title"] = 'JakSAFE Impact Class Config'
    
    if request.method == "POST":
        # handle form submit
        return HttpResponse("form submit")
    else:
        return render_to_response(template, RequestContext(request, context_dict))
