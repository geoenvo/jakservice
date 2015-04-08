from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.db import connection, transaction
from datetime import datetime
from django.conf import settings
import os
import csv
import sys
import subprocess
from report.forms import ImpactClassForm
from django.contrib import messages

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

def valid_date(t0, t1, adhoc=False):
    if (t0 != '' and t1 != ''):
        start = s = end = e = None
        
        # special format for passing to adhoc calc
        if (adhoc == True):
            start = datetime.strptime(t0, '%Y-%m-%d %H:%M:%S')
            end = datetime.strptime(t1, '%Y-%m-%d %H:%M:%S')
            s = start.strftime('%y%m%d%H%M%S')
            e = end.strftime('%y%m%d%H%M%S')
            
        else:
            t0 += ' 00:00:00' # '2015-01-01 00:00:00'
            t1 += ' 23:59:59' # '2015-01-01 23:59:59'
            start = datetime.strptime(t0, '%Y-%m-%d %H:%M:%S')
            end = datetime.strptime(t1, '%Y-%m-%d %H:%M:%S')
        
        if (start > end):
            return False
        
        return {'t0': start, 't1': end, 's': s, 'e': e}
    
    return False
    
def report_auto(request, template='report/report_auto.html'):
    context_dict = {}
    context_dict["page_title"] = 'JakSAFE Automatic Report'
    context_dict["errors"] = []
    context_dict["successes"] = []
    
    cursor = connection.cursor()
    
    if request.method == "POST":
        # handle form submit
        t0 = request.POST.get('t0')
        t1 = request.POST.get('t1')
        
        # check if given date is valid, start date < end date
        date_range = valid_date(t0, t1)
        
        if (date_range != False):
            # process filter
            print "DEBUG t0 = %s, t1 = %s" % (date_range['t0'], date_range['t1'])
            
            cursor.execute("SELECT id, t0, t1, damage, loss FROM auto_calc WHERE t0 >= '%s' AND t1 <= '%s' ORDER BY id DESC" % (date_range['t0'], date_range['t1']))
            
            resultset = dictfetchall(cursor)
            
            context_dict["auto_calc"] = resultset
            
            messages.add_message(request, messages.INFO, "Showing reports for date period: %s - %s" % (date_range['t0'], date_range['t1']))
        else:
            # invalid date range given, set flash message and redirect
            messages.add_message(request, messages.ERROR, "Please input a valid date period.")
            
            return HttpResponseRedirect(reverse('report_auto'))
    else:
        cursor.execute("SELECT id, t0, t1, damage, loss FROM auto_calc ORDER BY id DESC")
        
        resultset = dictfetchall(cursor)
        
        print resultset
        print 'DEBUG %s' % settings.PROJECT_ROOT
        
        context_dict["jakservice_auto_output_report_url"] = settings.JAKSERVICE_AUTO_OUTPUT_URL + settings.JAKSERVICE_REPORT_DIR
        context_dict["jakservice_auto_output_log_url"] = settings.JAKSERVICE_AUTO_OUTPUT_URL + settings.JAKSERVICE_LOG_DIR
        context_dict["auto_calc"] = resultset
        
    return render_to_response(template, RequestContext(request, context_dict))

def report_adhoc(request, template='report/report_adhoc.html'):
    context_dict = {}
    context_dict["page_title"] = 'JakSAFE Ad Hoc DaLA Report'
    context_dict["errors"] = []
    context_dict["successes"] = []
    
    cursor = connection.cursor()
    
    # adhoc calc date range posted
    if request.method == "POST":
        # handle form submit
        t0 = request.POST.get('t0')
        t1 = request.POST.get('t1')
        
        date_range = valid_date(t0, t1, adhoc=True)
        
        if (date_range != False):
            # process filter
            print "DEBUG t0 = %s, t1 = %s" % (date_range['t0'], date_range['t1'])
            print "DEBUG s = %s, e = %s" % (date_range['s'], date_range['e'])
            
            #?? query fl_event for t0 <= request_time <= t1
            cursor.execute("SELECT count(id) AS flood_reports FROM fl_event WHERE request_time >= '%s' AND request_time <= '%s'" % (date_range['t0'], date_range['t1']))
            
            flood_reports = dictfetchall(cursor)
            flood_reports_count = int(flood_reports[0]['flood_reports'])
            
            # only run DALA subproc if there are flood report in the period
            if flood_reports_count > 0:
                print "DEBUG flood reports = %s" % flood_reports_count
                
                #?? 20150327 no need, let jakservice do it
                #?? create new record in adhoc_calc(t0=t0, t1=t1, damage=null, loss=null)
                ## cursor.execute("INSERT INTO adhoc_calc(t0, t1, damage, loss) VALUES ('%s', '%s', NULL, NULL)" % (date_range['t0'], date_range['t1']))
                ## transaction.commit_unless_managed()
                ## last_row_id = cursor.lastrowid
                ## print 'DEBUG last row id = %s' % last_row_id
                
                print 'DEBUG Executing DALA subproc!'
                ## print os.path.dirname(os.path.abspath(__file__))
                
                jakservice_script_dir = os.path.join(settings.PROJECT_ROOT, 'jakservice/')
                
                print jakservice_script_dir
                
                ## run_dalla_auto_script = jakservice_script_dir + 'run_dalla_auto.py'
                run_dalla_adhoc_script = jakservice_script_dir + 'run_dalla_adhoc.py'
                
                print run_dalla_adhoc_script
                
                #?? execute subproc adhoc_dala_script(t0, t1)
                ## subprocess.Popen(['/home/user/.virtualenvs/jakservice/bin/python', '/home/user/.virtualenvs/jakservice/src1/save_fl_flood_dev.py', '>>', '/home/user/.virtualenvs/jakservice/src1/output/save_fl_flood_dev.log'])
                
                process = subprocess.Popen([settings.PYTHON_EXEC, run_dalla_adhoc_script, '-s', date_range['s'], '-e', date_range['e']])
                
                messages.add_message(request, messages.SUCCESS, 'Adhoc calculation started for date period [%s - %s]. This may take a moment.' % (date_range['t0'], date_range['t1']))
            
                return HttpResponseRedirect(reverse('report_adhoc'))
            else:
                print 'DEBUG no flood reports found!'
                
                messages.add_message(request, messages.ERROR, "No flood reports found for date period: %s - %s" % (date_range['t0'], date_range['t1']))
            
                return HttpResponseRedirect(reverse('report_adhoc'))
        else:
            # invalid date range given, set flash message and redirect
            messages.add_message(request, messages.ERROR, "Please input a valid date period.")
            
            return HttpResponseRedirect(reverse('report_adhoc'))
    else:
        #?? if latest adhoc_calc record damage/loss == null, set inprogress context, in template inprogress sets meta refresh in adhoc_calc template
        
        #?? query and return adhoc_calc context
        cursor.execute("SELECT id, t0, t1, damage, loss FROM adhoc_calc ORDER BY id DESC")
        
        resultset = dictfetchall(cursor)
        
        context_dict["jakservice_adhoc_output_report_url"] = settings.JAKSERVICE_ADHOC_OUTPUT_URL + settings.JAKSERVICE_REPORT_DIR
        context_dict["jakservice_adhoc_output_log_url"] = settings.JAKSERVICE_ADHOC_OUTPUT_URL + settings.JAKSERVICE_LOG_DIR
        context_dict["adhoc_calc"] = resultset
        
    return render_to_response(template, RequestContext(request, context_dict))

def report_impact_config(request, template='report/report_impact_config.html'):
    context_dict = {}
    context_dict["page_title"] = 'JakSAFE Impact Class Config'
    context_dict["errors"] = []
    context_dict["successes"] = []
    context_dict["form"] = None
    
    if request.method == "POST":
        # handle form submit
        form = ImpactClassForm(request.POST, request.FILES)
        
        # check if valid file type and size limit
        if form.is_valid():
            print 'DEBUG valid form'
            print request.FILES['impact_class_file']
            
            # write uploaded file to impact class config dir
            file_uploaded = handle_file_upload(request.FILES['impact_class_file'])
            
            if (file_uploaded == True):
                # set flash message
                messages.add_message(request, messages.SUCCESS, 'Upload successful.')
            else:
                messages.add_message(request, messages.ERROR, 'Upload failed.')
            
            return HttpResponseRedirect(reverse('report_impact_config'))
        else:
            print 'DEBUG invalid form'
            
            messages.add_message(request, messages.ERROR, 'Upload failed.')
            
            return HttpResponseRedirect(reverse('report_impact_config'))
    else:
        form = ImpactClassForm()
        context_dict["form"] = form
        
    print 'DEBUG %s' % settings.JAKSERVICE_IMPACT_CLASS_FILEPATH
    
    # read and output impact class csv file content
    if (os.path.isfile(settings.JAKSERVICE_IMPACT_CLASS_FILEPATH) == True):
        csvlist = []
        try:
            with open(settings.JAKSERVICE_IMPACT_CLASS_FILEPATH, 'rb') as csvfile:
                csvreader = csv.DictReader(csvfile)
                for row in csvreader:
                    csvlist.append(row)
            
            context_dict["csvlist"] = csvlist
        except IOError:
            print 'DEBUG IO exception when reading impact class csv file'
    
    #return HttpResponse("form submit")
    
    return render_to_response(template, RequestContext(request, context_dict))
    
def handle_file_upload(file_upload):
    # overwrite existing impact clas csv file
    try:
        with open(settings.JAKSERVICE_IMPACT_CLASS_FILEPATH, 'wb+') as destination:
            for chunk in file_upload.chunks():
                destination.write(chunk)
    except IOError:
        print 'DEBUG IO exception when writing file upload'
        return False
    else:
        return True