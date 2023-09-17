import ConfigParser

from reader import InfluxDBReader
from data_processor import AnomolyDetector, NoProcessing
from report_generator import PDFGenerator,DocGenerator

# Data-Source >> add_argument('DataSource', choices=['InfluxDB', 'File'],default='InfluxDB')
    #InfluxDB
    #Hadoop
    #File

#Access-Type >>  add_argument('AccessType', choices=['Developer', 'Manager', 'Default'],default='Default')
    #Developer
    #Manager
    #Default

#subparsers.add_parser('query', help='a help')
#parser_a.add_argument('-m measurement', type=int, help='bar help')
#parser_a.add_argument('--baz', choices='XYZ', help='baz help')

#Query
    #Measurement
    #Host
    #Tag,Field
    #Time
    #Catagory or grouping
    #Limit
    #ORDER

#Process-Type >>> -p Anomaly, Forecasting, Compare
    #Anomay Detection
    #Forcasting
    #Comparison >> custorm action

#Data-Visualization-Type >>>
    #Chart
        #Bar Chart, Pie Chart(Default), Histogram
    #Table
        #Dependeds on data value
    #Text
        #Summary Text

#Report-TYpe
    #PDF(Default)
    #DOC
    #TEXT

#Access-Type|Data-Source|Query|Process-Type|Data-Visualization-Type|Report-Type

#Manager|Varnish|"select cache_hit from varnish"|-|Pie|PDF
#Manager|Varnish|"select cache_hit from varnish"|-|Pie,table|PDF,DOC
#Manager|Varnish|"select cache_hit from varnish"|-|Pie, bar,summary|PDF

#Manager|Varnish|"select cache_hit from varnish"|Anomaly|Pie,bar|PDF


def config_section_map(config,sections):
    dict1 = {}
    for section in sections:
        options = config.options(section)
        for option in options:
            try:
                dict1[option] = config.get(section, option)
                if dict1[option] == -1:
                    print("skip: %s" % option)
            except:
                print("exception on %s!" % option)
                dict1[option] = None
    return dict1


conf_file_path = '../conf'

request={
    'access_type':'Manager',
    'Data_source':'InfluxDB',
    'query':{
            'measurement': ['Varnish'],
            'host': ['localhost'],
            'field':['cache_hit'],
            'time_filter':['from_data','to_date'],
            'more_filtering':{
                'group_by':[],
                'Having':[],
                'Limit':[],
                'Order':[]
            }
        },
    'process_type':{
        'anomaly_detection':'Simple Threshold Model',
        'forcasting':[''],
        'comparison':{
            'query':{
                'measurement': ['Varnish'],
                'host': ['localhost'],
                'field':'cache_hit',
                'time_filter':['from_data','to_date'],
                'more_filtering':{
                    'group_by':[],
                    'Having':[],
                    'Limit':[],
                    'Order':[]
                }
            }
        }
    },
    'visualization_type':{
        'Chart':[],
        'Table': ['Management'],
        'Text': ['']
    },
    'Report_type':['PDF','DOC','TEXT']
}


class Application:
    def __init__(self, params):
        self.data_source = params.get('data_source','InfluxDB')
        self.influxdb_host =params.get('host','localhost')
        self.influxdb_port =params.get('port','8086')
        self.influxdb_name =params.get('db_name','InfluxDB')

    def set_policy(self):
        pass

    def __call__(self, request):
        self.request = request
        reporter = PDFGenerator()
        dprocessor = NoProcessing()

        dprocessor.register_report_generator(reporter)
        rdr = InfluxDBReader(self)
        rdr.register_data_processor(dprocessor)
        rdr.read(request)

def run():
    config = ConfigParser.ConfigParser()
    config.read('../config')
    cfg_params = config_section_map(config,sections=config.sections())
    app = Application(cfg_params)
    app(request)

if __name__ == '__main__':
    run()


















# report_gen2 = report_generator.DocGenerator()
# data_psor.register_report_generator(report_gen2)