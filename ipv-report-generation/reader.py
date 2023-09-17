from influxdb import DataFrameClient
from datetime import timedelta, datetime
import pandas as pd

from observer import Subject
from influx_func import Max, Min, Mean
from influx_query import Query
from utils import get_formatted_time


class Reader(Subject):
    data_processors = []

    def read(self, request):
        raise NotImplementedError("must be implemented")

    def register_data_processor(self, processor):
        try:
            if processor not in self.data_processors:
                self.data_processors.append(processor)
                processor.register_subject(self)
            else:
                raise ValueError
        except ValueError:
            print "ERROR: Observer already subscribe to Subject"
            raise ValueError

    def remove_data_processor(self, processor):
        try:
            if processor not in self.data_processors:
                processor.remove_subject()
                self.data_processors.remove(processor)
            else:
                raise ValueError
        except ValueError:
            print "Error: Observer currently not subscribed to Subject"
            raise ValueError


    def notify_data_processors(self, request):
        for processor in self.data_processors:
            processor.update(request)


class InfluxDBReader (Reader):
    def __init__(self, app):
        self.data_source = app.data_source
        self.influxdb_host = app.influxdb_host
        self.influxdb_port = app.influxdb_port
        self.influxdb_name = app.influxdb_name

    def read(self, request):
        self.management_reader(request)
        # upperDate = datetime.now()
        # lowerDate = 28
        # query = Query(Mean('usage_system').as_("avg_cpu"), Max('usage_system').as_("max_cpu"), Min('usage_system').as_("min_cpu")).from_('cpu').where(time__gt=upperDate - timedelta(days=lowerDate)).group_by(time=timedelta(days=7))
        # max_min_query = Query(Max('usage_system').as_('max_cpu'), Min('usage_system').as_('min_cpu')).from_('cpu').where(time__gt=upperDate - timedelta(days=lowerDate))
        # max_col = ['max_cpu']
        # min_col = ['min_cpu']
        # client = DataFrameClient(self.influxdb_host, self.influxdb_port, database=self.influxdb_name)
        # raw_data = client.query(str(query))
        # max_min_data = client.query(str(max_min_query))
        # client.close()
        #
        # dataframe = join_dataframes(raw_data)
        # print(dataframe)
        # set_yrange(max_min_data, max_col, min_col)
        # set_ticks(dataframe)
        #
        # self.data = dataframe
        # self.notify_data_processors(request)

    def management_reader(self, request):
        upperDate = datetime.now()
        lowerDate = 7
        field1 = 'usage_user'
        field2 = 'used_percent'
        field3 = 'bytes_sent'
        query = Query(Mean(field1).as_(field1), Mean(field2).as_(field2), Mean(field3).as_(field3)).from_('cpu', 'mem', 'net').where(time__gt=upperDate - timedelta(days=lowerDate)).group_by(time=timedelta(minutes=1))
        print(query)
        client = DataFrameClient(self.influxdb_host, self.influxdb_port, database=self.influxdb_name)
        raw_data = client.query(str(query))
        client.close()
        for key in raw_data.keys():
            df = raw_data[key]
            col_list = df[df.columns[0]].tolist()
            col_list.reverse()
            avg_list = []
            high_list = []
            low_list =[]
            interval = 7 * 24 * 60
            low = 0
            length = len(col_list)
            while(length > low):
                high = low + interval
                if(high > length):
                    high = length
                temp_list = col_list[low:high]
                temp_list = [temp for temp in temp_list if(str(temp) != 'nan')]
                low = high + 1
                if(key == 'net'):
                    count = 0
                    derivative_list  = []
                    derivative_list_length = len(temp_list) - 1
                    while(count <  derivative_list_length):
                        derivative_list.append(abs(temp_list[count + 1] - temp_list[count]))
                        count = count + 1
                    max_temp = max(derivative_list)
                    target_max = max_temp - (max_temp * 0.05)
                    min_temp = min(derivative_list)
                    target_min = min_temp + (min_temp * 0.05)
                    avg_list.append('{0:.1f}'.format((sum(derivative_list) / float(derivative_list_length)) / (1024 * 1024)) + ' MB/s')
                    duration_high_minutes = sum(i > target_max for i in derivative_list)
                    duration_high = get_formatted_time(duration_high_minutes)
                    high_list.append('{0:.1f}'.format(max_temp / (1024 * 1024)) + ' MB/s (' + duration_high + ')')
                    duration_low_minutes = sum(i < target_min for i in derivative_list)
                    duration_low = get_formatted_time(duration_low_minutes)
                    low_list.append('{0:.1f}'.format(min_temp / (1024 * 1024)) + ' MB/s (' + duration_low + ')')
                else:
                    max_temp = max(temp_list)
                    target_max = max_temp - (max_temp * 0.05)
                    min_temp = min(temp_list)
                    target_min = min_temp + (min_temp * 0.05)
                    # avg_list.append('{0:.2f}'.format(sum(temp_list) / float(len(temp_list))) + '%')
                    avg_list.append(str(int((sum(temp_list) / float(len(temp_list))))) + '%')
                    duration_high_minutes = sum(i > target_max for i in temp_list)
                    duration_high = get_formatted_time(duration_high_minutes)
                    # high_list.append('{0:.2f}'.format(target_max) + '% to ' + '{0:.2f}'.format(max_temp) + '% (' + duration_high + ')')
                    high_list.append(str(int((max_temp))) + '% (' + duration_high + ')')
                    duration_low_minutes = sum(i < target_min for i in temp_list)
                    duration_low = get_formatted_time(duration_low_minutes)
                    # low_list.append('{0:.2f}'.format(min_temp) + '% to ' + '{0:.2f}'.format(target_min) + '% (' + duration_low + ')')
                    low_list.append(str(int((min_temp))) + '% (' + duration_low + ')')
            week_list = range(1, len(high_list))
            week_list.append(len(high_list))
            dataframe = pd.DataFrame()
            dataframe[key] = []
            dataframe['Week'] = week_list
            dataframe['Average'] = avg_list
            dataframe['High'] = high_list
            dataframe['Low'] = low_list
            print(dataframe)
            self.data = dataframe
            self.notify_data_processors(request)


class FileReader (Reader):
    def __init__(self, config):
        pass

    def read(self, request):
        # TODO
        # read
        data = None
        self.notify_data_processors(data, request)