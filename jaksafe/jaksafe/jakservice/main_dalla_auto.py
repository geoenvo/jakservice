__AUTHOR__= 'FARIZA DIAN PRASETYO'

from jaksafe import global_conf_parser
from jaksafe import qgis_install_path

from config_folder import input_folder
from config_folder import hazard_kelas_folder
from config_folder import input_boundary_folder
from config_folder import input_exposure_folder
from config_folder import input_exposure_shapefile_folder
from config_folder import auto_output_folder

from auto_preprocessing.preprocess_fl_report import *
from auto_preprocessing.auto_calc_function import *

from impact_analysis.hazard_compilation_function import *
from impact_analysis.hazard_analysis_class import HazardLayer
from impact_analysis.exposure_analysis_class import ExposureLayer

import Time as t
import requests
import sys
import datetime
import time

# Package QGIS
from qgis.core import *
import qgis.utils
from PyQt4.QtCore import *

from Time import formatted_date_to_timestamp
from Time import timestamp_to_formatted_date
from Time import timestamp_to_date_time

from header_config_variable import std_time_format

#input from data dims and database configuration
base_dims_url = global_conf_parser.get('dims_conf','url_dims')
table_name_event = global_conf_parser.get('database_configuration','table_name_event')
table_raw_name_event = global_conf_parser.get('database_configuration','table_raw_name_event')
table_name_autocalc = global_conf_parser.get('database_configuration','table_name_autocalc')

report_hazard_summary_name = global_conf_parser.get('file_output','output_hazard_summary_report')
report_RT_name = global_conf_parser.get('file_output','output_rt_report')
report_RW_name = global_conf_parser.get('file_output','output_rw_report')

#input kelas hazard
kelas_hazard_config_name = global_conf_parser.get('file_input','input_kelas')
kelas_hazard_file = hazard_kelas_folder + '/' + kelas_hazard_config_name

#input layer for hazard
boundary_name = global_conf_parser.get('file_input','input_boundary_layer')
input_boundary_layer_file = input_boundary_folder + '/' + boundary_name

#Output layer for hazard
output_hazard_layer_name = global_conf_parser.get('file_output','output_hazard')

#input layer for building exposure
building_exposure_layer_name = global_conf_parser.get('file_input','input_building_exposure')
input_building_exposure_layer_file = input_exposure_shapefile_folder + '/' + building_exposure_layer_name

#output layer for building exposure
output_building_exposure_layer_name = global_conf_parser.get('file_output','output_building_exposure')

#input layer for road exposure
road_exposure_layer_name = global_conf_parser.get('file_input','input_road_exposure')
input_road_exposure_layer_file = input_exposure_shapefile_folder + '/' + road_exposure_layer_name

#output layer for building exposure
output_road_exposure_layer_name = global_conf_parser.get('file_output','output_road_exposure')

max_observe = 2
base_folder_output = auto_output_folder


def create_fl_report_and_compilation_report(df_fl_event,t0,t1):
    try:
        df_all_units = df_fl_event
        
        ## create fl report for RT,RW,and summary in csv 
        create_summary_fl_report(df_all_units,\
                                 t.Time(t0),\
                                 t.Time(t1),\
                                 report_hazard_summary_name,\
                                 report_RT_name,\
                                 report_RW_name,\
                                 base_folder_output)

        ## create compilation report
        df_compiled_hazard = compiling_hazard_fl_in_folder(df_all_units,\
                                                           kelas_hazard_file,\
                                                           base_folder_output,\
                                                           t.Time(t0),\
                                                           t.Time(t1))
                                                           
        ## create shp hazard layer
        obj_layer = HazardLayer(input_boundary_layer_file,\
                                      kelas_hazard_file,\
                                      output_hazard_layer_name,\
                                      base_folder_output,\
                                      t.Time(t0),t.Time(t1))
                                                                               
        hazard_fl_layer = obj_layer.create_hazard_shp(df_compiled_hazard)                                                   
                                                                
    except Exception,e:
        print e
        sys.exit(1)

    return df_all_units,df_compiled_hazard


def calculate_impact_function(df_fl_event,t0,t1):
    try:
        df_all_units = df_fl_event
        ## create fl report
        create_fl_report(df_all_units,t.Time(t1),report_RT_name,report_RW_name,base_folder_output)

        ## Compiling hazard report
        #df_compiled = compiling_hazard_fl(df_all_units,kelas_hazard_file)
        df_compiled = compiling_hazard_fl_in_folder(df_all_units,kelas_hazard_file,base_folder_output,t.Time(t0),t.Time(t1))

        #QgsApplication.setPrefixPath(qgis_install_path, True)
        #QgsApplication.initQgis()

        obj_hazardlayer = HazardLayer(input_boundary_layer_file,kelas_hazard_file,output_hazard_layer_name,base_folder_output,t.Time(t0),t.Time(t1))
        hazard_fl_layer = obj_hazardlayer.create_hazard_shp(df_compiled)

        ## Creating building impact-exposure layer
        obj_buildingExposure = ExposureLayer(input_building_exposure_layer_file,base_folder_output,'building',t.Time(t0),t.Time(t1))
        obj_buildingExposure.set_building_exposure_layer_output(output_building_exposure_layer_name)
        print "Intersecting exposure building with hazard ...."
        obj_buildingExposure.intersect_building_exposure_with_hazard(hazard_fl_layer)

        obj_roadExposure = ExposureLayer(input_road_exposure_layer_file,base_folder_output,'road',t.Time(t0),t.Time(t1))
        obj_roadExposure.create_exposure_road_layer(output_road_exposure_layer_name,hazard_fl_layer)
        print "Intersecting exposure road with hazard ...."
        obj_roadExposure.intersect_road_exposure_with_hazard(hazard_fl_layer)

        #QgsApplication.exitQgis()

    except Exception,e:
        print e
        sys.exit(1)
    return obj_buildingExposure,obj_roadExposure

def formatted_date_to_timestamp(input_date,time_format):
        return int(time.mktime(datetime.datetime.strptime(input_date,time_format).timetuple()))

def main_impact_analysis_update(t0,t1,db_con):
    t0_timestamp_dims = formatted_date_to_timestamp(t0,std_time_format) + 1
    dims_format = '%Y%m%d%H'
    t0_dims = timestamp_to_formatted_date(t0_timestamp_dims,dims_format)
    print "Starting auto dalla impact analysis service ..."

    ## Crowling from the data dims
    #time_conf = 'starttime=%s&endtime=%s'%(t0,t1)
    time_conf = 'fromTime=%s'%(t0_dims)
    print time_conf

    dims_url = base_dims_url+'?'+ time_conf
    
    ## start comment here to bypass DIMS request
    response = requests.get(dims_url)

    print dims_url

    if response.status_code != 200:
        print "DIMS Service is not available...."
        print "Auto DALLA service is terminating ..."
        sys.exit(1)
    ## Get the data from dims
    dims_data = response.content


    print 'debugging dims data'
    
    #df_event_dims_raw,df_event_dims = convert_json_to_data_frame(dims_data,t1)
    df_event_dims_raw,df_event_dims = convert_json_to_data_frame_update(dims_data,t1)

    ## Checking data from DIMS
    if df_event_dims.empty:
        print "Empty data from gotten from dims ...."
        pass
    else:
        ## inserting dims data to fl_event database
        try:
            insert_dims_dataframe_to_database(df_event_dims_raw,df_event_dims,table_raw_name_event,table_name_event,db_con)
        except Exception,e:
            print e
            sys.exit(1)
    ## end comment here to bypass DIMS request
    
    ## Checking latest 2 days data from fl_event database
    df_last_fl = get_latest_fl_event(db_con,table_name_event,t.Time(t1),max_observe)
    ## If past 2 days is empty
    if df_last_fl.empty:
        print "Empty fl_event from last 2 days ...."
        base_folder_output = False
        pass

    ## If data in past 2 days is not empty, start to calculate impact function
    else:
        ## Check table 'auto_calc'
        t_last,loss = get_latest_report_status(db_con,table_name_autocalc)
        print 'get t_last: %s'%t_last

        if t_last !='' and loss !=None and loss > 0:
            t0 = t_last
            t0 = formatted_date_to_timestamp(t0,'%Y-%m-%d %H:%M:%S')
            t0 = t.Time(t0)
            t0 = t0.formattedTime()

        ## query from fl_event
        print "Fetching data from fl_event..."
        print t0
        print t1

        df_fl_event = get_fl_event(db_con,table_name_event,t0,t1)
        ## preprocessing df_fl_event
        df_all_units = preprocessing_the_hazard_data(df_fl_event)

        ## calculate impact function
        df_fl_hazard,df_hazard_compile = create_fl_report_and_compilation_report(df_fl_event,t0,t1)
        print df_fl_hazard
        print df_hazard_compile


        #obj_buildingExposure,obj_roadExposure = calculate_impact_function(df_fl_event,t0,t1)
    print t0
    print t1
    print "End of impact analysis service ..."

    return base_folder_output,t0

def main_impact_analysis_dump_csv(t0,t1,db_con):
    t0_timestamp_dims = formatted_date_to_timestamp(t0,std_time_format) + 1
    dims_format = '%Y%m%d%H'
    t0_dims = timestamp_to_formatted_date(t0_timestamp_dims,dims_format)
    print "Starting auto dalla impact analysis service ..."

    ## Crowling from the data dims
    #time_conf = 'starttime=%s&endtime=%s'%(t0,t1)
    time_conf = 'fromTime=%s'%(t0_dims)
    print time_conf

    dims_url = base_dims_url+'?'+ time_conf
    
    ## start comment here to bypass DIMS request
    response = requests.get(dims_url)

    print dims_url

    if response.status_code != 200:
        print "DIMS Service is not available...."
        print "Auto DALLA service is terminating ..."
        sys.exit(1)

    ## Get the data from dims
    dims_data = response.content

    #df_event_dims_raw,df_event_dims = convert_json_to_data_frame(dims_data,t1)
    df_event_dims_raw,df_event_dims = convert_json_to_data_frame_update(dims_data,t1)

    ## Checking data from DIMS
    if df_event_dims.empty:
        print "Empty data gotten from dims ...."
        pass
    else:
        ## inserting dims data to fl_event database
        try:
            insert_dims_dataframe_to_database(df_event_dims_raw,df_event_dims,table_raw_name_event,table_name_event,db_con)
        except Exception,e:
            print e
            sys.exit(1)
    ## end comment here to bypass DIMS request
    
    ## Checking latest 2 days data from fl_event database
    df_last_fl = get_latest_fl_event(db_con,table_name_event,t.Time(t1),max_observe)

    ## If past 2 days is empty
    if df_last_fl.empty:
        print "Empty fl_event from last 2 days ...."
        base_folder_output = False
        pass

    ## If data in past 2 days is not empty, start to calculate impact function
    else:
        ## Check table 'auto_calc'
        t_last,loss = get_latest_report_status(db_con,table_name_autocalc)
        print 'get t_last: %s'%t_last

        if t_last !='' and loss !=None and loss > 0:
            t0 = t_last
            t0 = formatted_date_to_timestamp(t0,'%Y-%m-%d %H:%M:%S')
            t0 = t.Time(t0)
            t0 = t0.formattedTime()

        ## query from fl_event
        print "Fetching data from fl_event..."
        df_fl_event = get_fl_event(db_con,table_name_event,t0,t1)
        ## preprocessing df_fl_event

        df_all_units = preprocessing_the_hazard_data(df_fl_event)
        ## calculate impact function

        ## calculate impact function
        df_fl_hazard,df_hazard_compile = create_fl_report_and_compilation_report(df_fl_event,t0,t1)

        #obj_buildingExposure,obj_roadExposure = calculate_impact_function(df_fl_event,t0,t1)

    print t0
    print t1
    print "End of impact analysis service ..."

    return base_folder_output,t0
