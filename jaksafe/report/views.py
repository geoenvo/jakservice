from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.db import connection, transaction
from datetime import datetime
from django.conf import settings
import os
import csv
import sys
import subprocess

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
    context_dict["errors"] = []
    
    cursor = connection.cursor()
    
    if request.method == "POST":
        # handle form submit
        t0 = request.POST.get('t0')
        t1 = request.POST.get('t1')
        
        date_range = valid_date(t0, t1)
        
        if (date_range != False):
            # process filter
            print "DEBUG t0 = %s, t1 = %s" % (date_range['t0'], date_range['t1'])
            
            cursor.execute("SELECT id, t0, t1, damage, loss FROM auto_calc WHERE t0 >= '%s' AND t1 <= '%s' ORDER BY id DESC" % (date_range['t0'], date_range['t1']))
            
            resultset = dictfetchall(cursor)
            
            context_dict["date_range"] = date_range
            context_dict["auto_calc"] = resultset
        else:
            context_dict["errors"].append("Please input a valid date range.")
    else:
        cursor.execute("SELECT id, t0, t1, damage, loss FROM auto_calc ORDER BY id DESC")
        
        resultset = dictfetchall(cursor)
        
        print resultset
        print settings.PROJECT_ROOT
        
        context_dict["auto_calc"] = resultset
        
    return render_to_response(template, RequestContext(request, context_dict))

def report_adhoc(request, template='report/report_adhoc.html'):
    context_dict = {}
    context_dict["page_title"] = 'JakSAFE Ad Hoc DaLA Report'
    context_dict["errors"] = []
    
    cursor = connection.cursor()
    
    if request.method == "POST":
        # handle form submit
        t0 = request.POST.get('t0')
        t1 = request.POST.get('t1')
        
        date_range = valid_date(t0, t1)
        
        if (date_range != False):
            # process filter
            print "DEBUG t0 = %s, t1 = %s" % (date_range['t0'], date_range['t1'])
            
            #?? query fl_event for t0 <= request_time <= t1
            cursor.execute("SELECT count(id) AS flood_reports FROM fl_event WHERE request_time >= '%s' AND request_time <= '%s'" % (date_range['t0'], date_range['t1']))
            
            flood_reports = dictfetchall(cursor)
            flood_reports_count = int(flood_reports[0]['flood_reports'])
            
            # only run DALA subproc if there are flood report in the period
            if flood_reports_count > 0:
                print "DEBUG %s" % flood_reports_count
                
                #?? create new record in adhoc_calc(t0=t0, t1=t1, damage=null, loss=null)
                
                ## cursor.execute("INSERT INTO adhoc_calc(t0, t1, damage, loss) VALUES ('%s', '%s', NULL, NULL)" % (date_range['t0'], date_range['t1']))
                
                ## transaction.commit_unless_managed()
                
                ## last_row_id = cursor.lastrowid
                
                ## print 'DEBUG last row id = %s' % last_row_id
                
                print 'DEBUG Executing DALA subproc!'
                
                #?? execute subproc adhoc_dala_script(t0, t1, new_record_id)
                
                ## subprocess.Popen(['/home/user/.virtualenvs/jakservice/bin/python', '/home/user/.virtualenvs/jakservice/src1/save_fl_flood_dev.py', '>>', '/home/user/.virtualenvs/jakservice/src1/output/save_fl_flood_dev.log'])
            else:
                print 'DEBUG no flood reports found!'
                context_dict["errors"].append("No flood reports found for period: %s - %s" % (date_range['t0'], date_range['t1']))
                
            
            #?? query and return adhoc_calc context
            cursor.execute("SELECT id, t0, t1, damage, loss FROM adhoc_calc ORDER BY id DESC")
            resultset = dictfetchall(cursor)
            #?? if latest adhoc_calc record damage/loss == null, set inprogress context, in template inprogress sets meta refresh in adhoc_calc template
            
            context_dict["adhoc_calc"] = resultset
            
        else:
            context_dict["errors"].append("Please input a valid date range.")
    else:
        cursor.execute("SELECT id, t0, t1, damage, loss FROM adhoc_calc ORDER BY id DESC")
        
        resultset = dictfetchall(cursor)
        
        context_dict["adhoc_calc"] = resultset
        
    return render_to_response(template, RequestContext(request, context_dict))

def report_impact_config(request, template='report/report_impact_config.html'):
    context_dict = {}
    context_dict["page_title"] = 'JakSAFE Impact Class Config'
    
    if (os.path.isfile(settings.IMPACT_CLASS_CONFIG) == True):
        csvlist = []
        with open(settings.IMPACT_CLASS_CONFIG, 'rb') as csvfile:
            csvreader = csv.DictReader(csvfile)
            for row in csvreader:
                csvlist.append(row)
        
        context_dict["csvlist"] = csvlist
    
    if request.method == "POST":
        # handle form submit
        return HttpResponse("form submit")
    else:
        return render_to_response(template, RequestContext(request, context_dict))
