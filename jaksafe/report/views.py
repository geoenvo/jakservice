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
from report.forms import ImpactClassForm, AggregateForm, AssumptionsDamageForm, AssumptionsLossForm, AssumptionsAggregateForm, AssumptionsInsuranceForm, AssumptionsInsurancePenetrationForm, BoundaryForm, BuildingExposureForm, RoadExposureForm
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
            file_uploaded = handle_impact_config_upload(request.FILES['impact_class_file'])
            
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
        context_dict["impact_class_download_url"] = settings.JAKSERVICE_IMPACT_CLASS_URL + settings.JAKSERVICE_IMPACT_CLASS_FILENAME
        
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
    
def handle_impact_config_upload(file_upload):
    # overwrite existing impact class csv file
    try:
        with open(settings.JAKSERVICE_IMPACT_CLASS_FILEPATH, 'wb+') as destination:
            for chunk in file_upload.chunks():
                destination.write(chunk)
    except IOError:
        print 'DEBUG IO exception when writing file upload'
        return False
    else:
        return True

def report_assumptions_config(request, template='report/report_assumptions_config.html'):
    context_dict = {}
    context_dict["page_title"] = 'JakSAFE Assumptions Config'
    context_dict["errors"] = []
    context_dict["successes"] = []
    context_dict["form"] = None
    
    if request.method == "POST":
        # handle form submit
        form_damage = AssumptionsDamageForm(request.POST, request.FILES)
        form_loss = AssumptionsLossForm(request.POST, request.FILES)
        form_aggregate = AssumptionsAggregateForm(request.POST, request.FILES)
        form_insurance = AssumptionsInsuranceForm(request.POST, request.FILES)
        form_insurance_penetration = AssumptionsInsurancePenetrationForm(request.POST, request.FILES)
        
        if u'assumptions_damage_file' in request.FILES:
            if form_damage.is_valid():
                file_type = 'assumptions_damage_file'
                
                print 'DEBUG valid form'
                print request.FILES[file_type]
                
                file_uploaded = handle_assumptions_config_upload(request.FILES[file_type], type=file_type)
                
                if (file_uploaded == True):
                    messages.add_message(request, messages.SUCCESS, "'Assumptions Damage' upload successful.")
                else:
                    messages.add_message(request, messages.ERROR, "'Assumptions Damage' upload failed.")
            else:
                messages.add_message(request, messages.ERROR, "'Assumptions Damage' upload failed.")
        
        if u'assumptions_loss_file' in request.FILES:
            if form_loss.is_valid():
                file_type = 'assumptions_loss_file'
                
                print 'DEBUG valid form'
                print request.FILES[file_type]
                
                file_uploaded = handle_assumptions_config_upload(request.FILES[file_type], type=file_type)
                
                if (file_uploaded == True):
                    messages.add_message(request, messages.SUCCESS, "'Assumptions Loss' upload successful.")
                else:
                    messages.add_message(request, messages.ERROR, "'Assumptions Loss' upload failed.")
            else:
                messages.add_message(request, messages.ERROR, "'Assumptions Loss' upload failed.")
        
        if u'assumptions_aggregate_file' in request.FILES:
            if form_aggregate.is_valid():
                file_type = 'assumptions_aggregate_file'
                
                print 'DEBUG valid form'
                print request.FILES[file_type]
                
                file_uploaded = handle_assumptions_config_upload(request.FILES[file_type], type=file_type)
                
                if (file_uploaded == True):
                    messages.add_message(request, messages.SUCCESS, "'Assumptions Aggregate' upload successful.")
                else:
                    messages.add_message(request, messages.ERROR, "'Assumptions Aggregate' upload failed.")
            else:
                messages.add_message(request, messages.ERROR, "'Assumptions Aggregate' upload failed.")
        
        if u'assumptions_insurance_file' in request.FILES:
            if form_insurance.is_valid():
                file_type = 'assumptions_insurance_file'
                
                print 'DEBUG valid form'
                print request.FILES[file_type]
                
                file_uploaded = handle_assumptions_config_upload(request.FILES[file_type], type=file_type)
                
                if (file_uploaded == True):
                    messages.add_message(request, messages.SUCCESS, "'Assumptions Insurance' upload successful.")
                else:
                    messages.add_message(request, messages.ERROR, "'Assumptions Insurance' upload failed.")
            else:
                messages.add_message(request, messages.ERROR, "'Assumptions Insurance' upload failed.")
        
        if u'assumptions_insurance_penetration_file' in request.FILES:    
            if form_insurance_penetration.is_valid():
                file_type = 'assumptions_insurance_penetration_file'
                
                print 'DEBUG valid form'
                print request.FILES[file_type]
                
                file_uploaded = handle_assumptions_config_upload(request.FILES[file_type], type=file_type)
                
                if (file_uploaded == True):
                    messages.add_message(request, messages.SUCCESS, "'Assumptions Insurance Penetration' upload successful.")
                else:
                    messages.add_message(request, messages.ERROR, "'Assumptions Insurance Penetration' upload failed.")
            else:
                messages.add_message(request, messages.ERROR, "'Assumptions Insurance Penetration' upload failed.")
        
        return HttpResponseRedirect(reverse('report_assumptions_config'))
    else:
        assumptions_damage_form = AssumptionsDamageForm()
        context_dict["assumptions_damage_form"] = assumptions_damage_form
        
        assumptions_loss_form = AssumptionsLossForm()
        context_dict["assumptions_loss_form"] = assumptions_loss_form
        
        assumptions_aggregate_form = AssumptionsAggregateForm()
        context_dict["assumptions_aggregate_form"] = assumptions_aggregate_form
        
        assumptions_insurance_form = AssumptionsInsuranceForm()
        context_dict["assumptions_insurance_form"] = assumptions_insurance_form
        
        assumptions_insurance_penetration_form = AssumptionsInsurancePenetrationForm()
        context_dict["assumptions_insurance_penetration_form"] = assumptions_insurance_penetration_form
    
    # read and output assumptions damage csv file content
    if (os.path.isfile(settings.JAKSERVICE_ASSUMPTIONS_DAMAGE_FILEPATH) == True):
        context_dict["assumptions_damage_download_url"] = settings.JAKSERVICE_ASSUMPTIONS_URL + settings.JAKSERVICE_ASSUMPTIONS_DAMAGE_FILENAME
        
        try:
            csvlist = []
            with open(settings.JAKSERVICE_ASSUMPTIONS_DAMAGE_FILEPATH, 'rb') as csvfile:
                csvreader = csv.DictReader(csvfile)
                for row in csvreader:
                    csvlist.append(row)
            
            context_dict["assumptions_damage_csv"] = csvlist
        except IOError:
            print 'DEBUG IO exception when reading assumptions damage csv file'
    
    # read and output assumptions loss csv file content
    if (os.path.isfile(settings.JAKSERVICE_ASSUMPTIONS_LOSS_FILEPATH) == True):
        context_dict["assumptions_loss_download_url"] = settings.JAKSERVICE_ASSUMPTIONS_URL + settings.JAKSERVICE_ASSUMPTIONS_LOSS_FILENAME
        
        try:
            csvlist = []
            with open(settings.JAKSERVICE_ASSUMPTIONS_LOSS_FILEPATH, 'rb') as csvfile:
                csvreader = csv.DictReader(csvfile)
                for row in csvreader:
                    csvlist.append(row)
            
            context_dict["assumptions_loss_csv"] = csvlist
        except IOError:
            print 'DEBUG IO exception when reading assumptions loss csv file'
    
    # read and output assumptions aggregate csv file content
    if (os.path.isfile(settings.JAKSERVICE_ASSUMPTIONS_AGGREGATE_FILEPATH) == True):
        context_dict["assumptions_aggregate_download_url"] = settings.JAKSERVICE_ASSUMPTIONS_URL + settings.JAKSERVICE_ASSUMPTIONS_AGGREGATE_FILENAME
        
        try:
            csvlist = []
            with open(settings.JAKSERVICE_ASSUMPTIONS_AGGREGATE_FILEPATH, 'rb') as csvfile:
                csvreader = csv.DictReader(csvfile)
                for row in csvreader:
                    csvlist.append(row)
            
            context_dict["assumptions_aggregate_csv"] = csvlist
        except IOError:
            print 'DEBUG IO exception when reading assumptions loss csv file'
    
    # read and output assumptions insurance csv file content
    if (os.path.isfile(settings.JAKSERVICE_ASSUMPTIONS_INSURANCE_FILEPATH) == True):
        context_dict["assumptions_insurance_download_url"] = settings.JAKSERVICE_ASSUMPTIONS_URL + settings.JAKSERVICE_ASSUMPTIONS_INSURANCE_FILENAME
        
        try:
            csvlist = []
            with open(settings.JAKSERVICE_ASSUMPTIONS_INSURANCE_FILEPATH, 'rb') as csvfile:
                csvreader = csv.DictReader(csvfile)
                for row in csvreader:
                    csvlist.append(row)
            
            context_dict["assumptions_insurance_csv"] = csvlist
        except IOError:
            print 'DEBUG IO exception when reading assumptions insurance csv file'
    
    # read and output assumptions insurance penetration csv file content
    if (os.path.isfile(settings.JAKSERVICE_ASSUMPTIONS_INSURANCE_PENETRATION_FILEPATH) == True):
        context_dict["assumptions_insurance_penetration_download_url"] = settings.JAKSERVICE_ASSUMPTIONS_URL + settings.JAKSERVICE_ASSUMPTIONS_INSURANCE_PENETRATION_FILENAME
        
        try:
            csvlist = []
            with open(settings.JAKSERVICE_ASSUMPTIONS_INSURANCE_PENETRATION_FILEPATH, 'rb') as csvfile:
                csvreader = csv.DictReader(csvfile)
                for row in csvreader:
                    csvlist.append(row)
            
            context_dict["assumptions_insurance_penetration_csv"] = csvlist
        except IOError:
            print 'DEBUG IO exception when reading assumptions insurance penetration csv file'
    
    #return HttpResponse("form submit")
    
    return render_to_response(template, RequestContext(request, context_dict))

def handle_assumptions_config_upload(file_upload, type):
    # overwrite existing aggregate csv file
    try:
        upload_path = None
        
        if type == 'assumptions_damage_file':
            upload_path = settings.JAKSERVICE_ASSUMPTIONS_DAMAGE_FILEPATH
        elif type == 'assumptions_loss_file':
            upload_path = settings.JAKSERVICE_ASSUMPTIONS_LOSS_FILEPATH
        elif type == 'assumptions_aggregate_file':
            upload_path = settings.JAKSERVICE_ASSUMPTIONS_AGGREGATE_FILEPATH
        elif type == 'assumptions_insurance_file':
            upload_path = settings.JAKSERVICE_ASSUMPTIONS_INSURANCE_FILEPATH
        elif type == 'assumptions_insurance_penetration_file':
            upload_path = settings.JAKSERVICE_ASSUMPTIONS_INSURANCE_PENETRATION_FILEPATH
        
        if upload_path == None:
            return False
        
        with open(upload_path, 'wb+') as destination:
            for chunk in file_upload.chunks():
                destination.write(chunk)
        
    except IOError:
        print 'DEBUG IO exception when writing file upload'
        return False
    else:
        return True

def report_aggregate_config(request, template='report/report_aggregate_config.html'):
    context_dict = {}
    context_dict["page_title"] = 'JakSAFE Aggregate Config'
    context_dict["errors"] = []
    context_dict["successes"] = []
    context_dict["form"] = None
    
    if request.method == "POST":
        # handle form submit
        form = AggregateForm(request.POST, request.FILES)
        
        # check if valid file type and size limit
        if form.is_valid():
            print 'DEBUG valid form'
            print request.FILES['aggregate_file']
            
            # write uploaded file to assumptions config dir
            file_uploaded = handle_aggregate_config_upload(request.FILES['aggregate_file'])
            
            if (file_uploaded == True):
                # set flash message
                messages.add_message(request, messages.SUCCESS, 'Upload successful.')
            else:
                messages.add_message(request, messages.ERROR, 'Upload failed.')
            
            return HttpResponseRedirect(reverse('report_aggregate_config'))
        else:
            print 'DEBUG invalid form'
            
            messages.add_message(request, messages.ERROR, 'Upload failed.')
            
            return HttpResponseRedirect(reverse('report_aggregate_config'))
    else:
        form = AggregateForm()
        context_dict["form"] = form
        
    print 'DEBUG %s' % settings.JAKSERVICE_AGGREGATE_FILEPATH
    
    # read and output impact class csv file content
    if (os.path.isfile(settings.JAKSERVICE_AGGREGATE_FILEPATH) == True):
        context_dict["aggregate_download_url"] = settings.JAKSERVICE_AGGREGATE_URL + settings.JAKSERVICE_AGGREGATE_FILENAME
        
        csvlist = []
        try:
            with open(settings.JAKSERVICE_AGGREGATE_FILEPATH, 'rb') as csvfile:
                csvreader = csv.DictReader(csvfile)
                for row in csvreader:
                    csvlist.append(row)
            
            context_dict["csvlist"] = csvlist
        except IOError:
            print 'DEBUG IO exception when reading aggregate csv file'
    
    #return HttpResponse("form submit")
    
    return render_to_response(template, RequestContext(request, context_dict))

def handle_aggregate_config_upload(file_upload):
    # overwrite existing aggregate csv file
    try:
        with open(settings.JAKSERVICE_AGGREGATE_FILEPATH, 'wb+') as destination:
            for chunk in file_upload.chunks():
                destination.write(chunk)
    except IOError:
        print 'DEBUG IO exception when writing file upload'
        return False
    else:
        return True

def report_boundary_config(request, template='report/report_boundary_config.html'):
    context_dict = {}
    context_dict["page_title"] = 'JakSAFE Boundary Config'
    context_dict["errors"] = []
    context_dict["successes"] = []
    context_dict["form"] = None
    
    if request.method == "POST":
        # handle form submit
        form_boundary = BoundaryForm(request.POST, request.FILES)
        
        if form_boundary.is_valid():
            print 'DEBUG valid form'
            
            shp_file_uploaded = handle_boundary_config_upload(request.FILES['boundary_shp_file'], settings.JAKSERVICE_BOUNDARY_SHP_FILEPATH)
            shx_file_uploaded = handle_boundary_config_upload(request.FILES['boundary_shx_file'], settings.JAKSERVICE_BOUNDARY_SHX_FILEPATH)
            dbf_file_uploaded = handle_boundary_config_upload(request.FILES['boundary_dbf_file'], settings.JAKSERVICE_BOUNDARY_DBF_FILEPATH)
            prj_file_uploaded = handle_boundary_config_upload(request.FILES['boundary_prj_file'], settings.JAKSERVICE_BOUNDARY_PRJ_FILEPATH)
            qpj_file_uploaded = handle_boundary_config_upload(request.FILES['boundary_qpj_file'], settings.JAKSERVICE_BOUNDARY_QPJ_FILEPATH)
            
            if (shp_file_uploaded == True):
                messages.add_message(request, messages.SUCCESS, "'Boundary SHP' upload successful.")
            else:
                messages.add_message(request, messages.ERROR, "'Boundary SHP' upload failed.")
            
            if (shx_file_uploaded == True):
                messages.add_message(request, messages.SUCCESS, "'Boundary SHX' upload successful.")
            else:
                messages.add_message(request, messages.ERROR, "'Boundary SHX' upload failed.")
            
            if (dbf_file_uploaded == True):
                messages.add_message(request, messages.SUCCESS, "'Boundary DBF' upload successful.")
            else:
                messages.add_message(request, messages.ERROR, "'Boundary DBF' upload failed.")
            
            if (prj_file_uploaded == True):
                messages.add_message(request, messages.SUCCESS, "'Boundary PRJ' upload successful.")
            else:
                messages.add_message(request, messages.ERROR, "'Boundary PRJ' upload failed.")
            
            if (qpj_file_uploaded == True):
                messages.add_message(request, messages.SUCCESS, "'Boundary QPJ' upload successful.")
            else:
                messages.add_message(request, messages.ERROR, "'Boundary QPJ' upload failed.")
        else:
            messages.add_message(request, messages.ERROR, "Boundary upload failed. Please upload the SHP, SHX, DBF, PRJ, and QPJ file set.")
        
        return HttpResponseRedirect(reverse('report_boundary_config'))
    else:
        context_dict["form"]  = BoundaryForm()
        
        if (os.path.isfile(settings.JAKSERVICE_BOUNDARY_SHP_FILEPATH) == True):
            context_dict["shp_download_url"]  = settings.JAKSERVICE_BOUNDARY_URL + settings.JAKSERVICE_BOUNDARY_SHP_FILENAME
        
        if (os.path.isfile(settings.JAKSERVICE_BOUNDARY_SHX_FILEPATH) == True):
            context_dict["shx_download_url"]  = settings.JAKSERVICE_BOUNDARY_URL + settings.JAKSERVICE_BOUNDARY_SHX_FILENAME
        
        if (os.path.isfile(settings.JAKSERVICE_BOUNDARY_DBF_FILEPATH) == True):
            context_dict["dbf_download_url"]  = settings.JAKSERVICE_BOUNDARY_URL + settings.JAKSERVICE_BOUNDARY_DBF_FILENAME
        
        if (os.path.isfile(settings.JAKSERVICE_BOUNDARY_PRJ_FILEPATH) == True):
            context_dict["prj_download_url"]  = settings.JAKSERVICE_BOUNDARY_URL + settings.JAKSERVICE_BOUNDARY_PRJ_FILENAME
        
        if (os.path.isfile(settings.JAKSERVICE_BOUNDARY_QPJ_FILEPATH) == True):
            context_dict["qpj_download_url"]  = settings.JAKSERVICE_BOUNDARY_URL + settings.JAKSERVICE_BOUNDARY_QPJ_FILENAME
    
    return render_to_response(template, RequestContext(request, context_dict))

def handle_boundary_config_upload(file_upload, upload_path):
    try:
        with open(upload_path, 'wb+') as destination:
            for chunk in file_upload.chunks():
                destination.write(chunk)
        
    except IOError:
        print 'DEBUG IO exception when writing file upload'
        return False
    else:
        return True

def report_exposure_config(request, template='report/report_exposure_config.html'):
    context_dict = {}
    context_dict["page_title"] = 'JakSAFE Exposure Config'
    context_dict["errors"] = []
    context_dict["successes"] = []
    context_dict["form"] = None
    
    if request.method == "POST":
        # handle form submit
        form_building_exposure = BuildingExposureForm(request.POST, request.FILES)
        form_road_exposure = RoadExposureForm(request.POST, request.FILES)
        
        if form_building_exposure.is_valid():
            print 'DEBUG valid form'
            
            shp_file_uploaded = handle_exposure_config_upload(request.FILES['building_exposure_shp_file'], settings.JAKSERVICE_BUILDING_EXPOSURE_SHP_FILEPATH)
            shx_file_uploaded = handle_exposure_config_upload(request.FILES['building_exposure_shx_file'], settings.JAKSERVICE_BUILDING_EXPOSURE_SHX_FILEPATH)
            dbf_file_uploaded = handle_exposure_config_upload(request.FILES['building_exposure_dbf_file'], settings.JAKSERVICE_BUILDING_EXPOSURE_DBF_FILEPATH)
            prj_file_uploaded = handle_exposure_config_upload(request.FILES['building_exposure_prj_file'], settings.JAKSERVICE_BUILDING_EXPOSURE_PRJ_FILEPATH)
            qpj_file_uploaded = handle_exposure_config_upload(request.FILES['building_exposure_qpj_file'], settings.JAKSERVICE_BUILDING_EXPOSURE_QPJ_FILEPATH)
            
            if (shp_file_uploaded == True):
                messages.add_message(request, messages.SUCCESS, "'Building Exposure SHP' upload successful.")
            else:
                messages.add_message(request, messages.ERROR, "'Building Exposure SHP' upload failed.")
            
            if (shx_file_uploaded == True):
                messages.add_message(request, messages.SUCCESS, "'Building Exposure SHX' upload successful.")
            else:
                messages.add_message(request, messages.ERROR, "'Building Exposure SHX' upload failed.")
            
            if (dbf_file_uploaded == True):
                messages.add_message(request, messages.SUCCESS, "'Building Exposure DBF' upload successful.")
            else:
                messages.add_message(request, messages.ERROR, "'Building Exposure DBF' upload failed.")
            
            if (prj_file_uploaded == True):
                messages.add_message(request, messages.SUCCESS, "'Building Exposure PRJ' upload successful.")
            else:
                messages.add_message(request, messages.ERROR, "'Building Exposure PRJ' upload failed.")
            
            if (qpj_file_uploaded == True):
                messages.add_message(request, messages.SUCCESS, "'Building Exposure QPJ' upload successful.")
            else:
                messages.add_message(request, messages.ERROR, "'Building Exposure QPJ' upload failed.")
        else:
            messages.add_message(request, messages.ERROR, "Building Exposure upload failed. Please upload the SHP, SHX, DBF, PRJ, and QPJ file set.")
        
        if form_road_exposure.is_valid():
            print 'DEBUG valid form'
            
            shp_file_uploaded = handle_exposure_config_upload(request.FILES['road_exposure_shp_file'], settings.JAKSERVICE_ROAD_EXPOSURE_SHP_FILEPATH)
            shx_file_uploaded = handle_exposure_config_upload(request.FILES['road_exposure_shx_file'], settings.JAKSERVICE_ROAD_EXPOSURE_SHX_FILEPATH)
            dbf_file_uploaded = handle_exposure_config_upload(request.FILES['road_exposure_dbf_file'], settings.JAKSERVICE_ROAD_EXPOSURE_DBF_FILEPATH)
            prj_file_uploaded = handle_exposure_config_upload(request.FILES['road_exposure_prj_file'], settings.JAKSERVICE_ROAD_EXPOSURE_PRJ_FILEPATH)
            qpj_file_uploaded = handle_exposure_config_upload(request.FILES['road_exposure_qpj_file'], settings.JAKSERVICE_ROAD_EXPOSURE_QPJ_FILEPATH)
            
            if (shp_file_uploaded == True):
                messages.add_message(request, messages.SUCCESS, "'Road Exposure SHP' upload successful.")
            else:
                messages.add_message(request, messages.ERROR, "'Road Exposure SHP' upload failed.")
            
            if (shx_file_uploaded == True):
                messages.add_message(request, messages.SUCCESS, "'Road Exposure SHX' upload successful.")
            else:
                messages.add_message(request, messages.ERROR, "'Road Exposure SHX' upload failed.")
            
            if (dbf_file_uploaded == True):
                messages.add_message(request, messages.SUCCESS, "'Road Exposure DBF' upload successful.")
            else:
                messages.add_message(request, messages.ERROR, "'Road Exposure DBF' upload failed.")
            
            if (prj_file_uploaded == True):
                messages.add_message(request, messages.SUCCESS, "'Road Exposure PRJ' upload successful.")
            else:
                messages.add_message(request, messages.ERROR, "'Road Exposure PRJ' upload failed.")
            
            if (qpj_file_uploaded == True):
                messages.add_message(request, messages.SUCCESS, "'Road Exposure QPJ' upload successful.")
            else:
                messages.add_message(request, messages.ERROR, "'Road Exposure QPJ' upload failed.")
        else:
            messages.add_message(request, messages.ERROR, "Road Exposure upload failed. Please upload the SHP, SHX, DBF, PRJ, and QPJ file set.")
        
        return HttpResponseRedirect(reverse('report_exposure_config'))
    else:
        context_dict["building_exposure_form"]  = BuildingExposureForm()
        context_dict["road_exposure_form"]  = RoadExposureForm()
        
        if (os.path.isfile(settings.JAKSERVICE_BUILDING_EXPOSURE_SHP_FILEPATH) == True):
            context_dict["building_exposure_shp_download_url"]  = settings.JAKSERVICE_EXPOSURE_URL + settings.JAKSERVICE_BUILDING_EXPOSURE_SHP_FILENAME
        
        if (os.path.isfile(settings.JAKSERVICE_BUILDING_EXPOSURE_SHX_FILEPATH) == True):
            context_dict["building_exposure_shx_download_url"]  = settings.JAKSERVICE_EXPOSURE_URL + settings.JAKSERVICE_BUILDING_EXPOSURE_SHX_FILENAME
        
        if (os.path.isfile(settings.JAKSERVICE_BUILDING_EXPOSURE_DBF_FILEPATH) == True):
            context_dict["building_exposure_dbf_download_url"]  = settings.JAKSERVICE_EXPOSURE_URL + settings.JAKSERVICE_BUILDING_EXPOSURE_DBF_FILENAME
        
        if (os.path.isfile(settings.JAKSERVICE_BUILDING_EXPOSURE_PRJ_FILEPATH) == True):
            context_dict["building_exposure_prj_download_url"]  = settings.JAKSERVICE_EXPOSURE_URL + settings.JAKSERVICE_BUILDING_EXPOSURE_PRJ_FILENAME
        
        if (os.path.isfile(settings.JAKSERVICE_BUILDING_EXPOSURE_QPJ_FILEPATH) == True):
            context_dict["building_exposure_qpj_download_url"]  = settings.JAKSERVICE_EXPOSURE_URL + settings.JAKSERVICE_BUILDING_EXPOSURE_QPJ_FILENAME
        
        if (os.path.isfile(settings.JAKSERVICE_ROAD_EXPOSURE_SHP_FILEPATH) == True):
            context_dict["road_exposure_shp_download_url"]  = settings.JAKSERVICE_EXPOSURE_URL + settings.JAKSERVICE_ROAD_EXPOSURE_SHP_FILENAME
        
        if (os.path.isfile(settings.JAKSERVICE_ROAD_EXPOSURE_SHX_FILEPATH) == True):
            context_dict["road_exposure_shx_download_url"]  = settings.JAKSERVICE_EXPOSURE_URL + settings.JAKSERVICE_ROAD_EXPOSURE_SHX_FILENAME
        
        if (os.path.isfile(settings.JAKSERVICE_ROAD_EXPOSURE_DBF_FILEPATH) == True):
            context_dict["road_exposure_dbf_download_url"]  = settings.JAKSERVICE_EXPOSURE_URL + settings.JAKSERVICE_ROAD_EXPOSURE_DBF_FILENAME
        
        if (os.path.isfile(settings.JAKSERVICE_ROAD_EXPOSURE_PRJ_FILEPATH) == True):
            context_dict["road_exposure_prj_download_url"]  = settings.JAKSERVICE_EXPOSURE_URL + settings.JAKSERVICE_ROAD_EXPOSURE_PRJ_FILENAME
        
        if (os.path.isfile(settings.JAKSERVICE_ROAD_EXPOSURE_QPJ_FILEPATH) == True):
            context_dict["road_exposure_qpj_download_url"]  = settings.JAKSERVICE_EXPOSURE_URL + settings.JAKSERVICE_ROAD_EXPOSURE_QPJ_FILENAME
    
    return render_to_response(template, RequestContext(request, context_dict))

def handle_exposure_config_upload(file_upload, upload_path):
    try:
        with open(upload_path, 'wb+') as destination:
            for chunk in file_upload.chunks():
                destination.write(chunk)
        
    except IOError:
        print 'DEBUG IO exception when writing file upload'
        return False
    else:
        return True