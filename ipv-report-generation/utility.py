from datetime import timedelta, datetime
import math
import time

class DateTimeInterval:

    ndays = 30
    nmonts = 12
    nminutes = 60
    nseconds = 60

    def get_interval(self, to_date, from_date, FMT='%Y-%m-%d %H:%M:%S'):
        tdelta = to_date - from_date
        if tdelta.days < 0:
            tdelta = timedelta(days=0, seconds=tdelta.seconds, microseconds=tdelta.microseconds)

        days = tdelta.days
        months = (tdelta.days / DateTimeInterval.ndays)
        days = (days % DateTimeInterval.ndays)
        hours = tdelta.seconds / (DateTimeInterval.nminutes * DateTimeInterval.nseconds)
        minutes = (tdelta.seconds % (DateTimeInterval.nminutes * DateTimeInterval.nseconds)) / DateTimeInterval.nminutes
        seconds = (tdelta.seconds % (DateTimeInterval.nminutes * DateTimeInterval.nseconds)) % DateTimeInterval.nseconds

        indx = 0
        interval = 0

        while indx <= 3 and interval == 0:
            level = []

            if indx == 0:
                total_time = 30 * months + days
                time_flag = 'days'
            elif indx == 1:
                total_time = 24 * days + hours
                time_flag = 'hours'
            elif indx == 2:
                total_time = (60 * hours + minutes)
                time_flag = 'minutes'
            else:
                interval = (60 * minutes + seconds) / 12
                if (interval <= 30):
                    interval = 30
                    time_flag = 'seconds'
                else:
                    interval = 1
                    time_flag = 'minutes'

                level.append(interval)
                level.append(time_flag)

                return level

            interval = total_time / 12.00
            if (total_time % 12 >= 9):
                interval = math.ceil(interval)
            else:
                interval = math.floor(interval)

            level.append(interval)
            level.append(time_flag)
            indx = indx + 1

        return level


    def datetime_range(self, end, start, delta):

        current = start
        while current < end + delta:
            yield current
            current += delta

    def get_dataframe_datetime(self, data, location):
        index_time = data.index[location]
        index_time = time.strptime(str(index_time).split("+")[0], '%Y-%m-%d %H:%M:%S')
        index_date = datetime(index_time.tm_year, index_time.tm_mon, index_time.tm_mday, index_time.tm_hour,
                              index_time.tm_min,
                              index_time.tm_sec)
        return index_date


    def get_position(self, data, start_date, interval, interval_type, num_interval, data_size=0):
        pos = []

        location = data_size / num_interval

        if interval_type == "minutes":
            next_time = start_date + timedelta(minutes=interval)
        elif interval_type == "hours":
            next_time = start_date + timedelta(hours=interval)
        elif interval_type == "days":
            next_time = start_date + timedelta(days=interval)
        else:
            next_time = start_date + timedelta(seconds=interval)

        start_date = self.get_dataframe_datetime(data, location)

        count = 0
        while start_date < next_time:
            start_date = start_date + timedelta(minutes=1)
            count = count + 1

        location = location + count
        if location >= data_size:
            return pos

        loc = 0
        indx = 1
        while loc < data_size:
            pos.append(loc)
            loc = location * indx
            indx = indx + 1

        return pos

    def get_xyticks(self, dataframe):

        data_size = len(dataframe.index) - 1
        start_date = self.get_dataframe_datetime(dataframe, 0)
        end_date = self.get_dataframe_datetime(dataframe, data_size)

        interval = self.get_interval(end_date, start_date)
        interval_type = interval[1]
        interval = int(interval[0])

        if interval_type == "days":
            dts = [dt.strftime('%m/%d') for dt in
                   self.datetime_range(end_date, start_date, timedelta(days=interval))]

        elif interval_type == "hours":
            dts = [dt.strftime('%d/%H') for dt in
                   self.datetime_range(end_date, start_date, timedelta(hours=interval))]

        elif interval_type == "minutes":
            dts = [dt.strftime('%H/%M') for dt in
                   self.datetime_range(end_date, start_date, timedelta(minutes=interval))]
        else:
            dts = [dt.strftime('%M/%S') for dt in
                   self.datetime_range(end_date, start_date, timedelta(seconds=interval))]

        position_list = self.get_position(dataframe, start_date, interval, interval_type, len(dts), data_size)

        scaled_df = dataframe.iloc[position_list, ]
        columns = {}
        for column_name in scaled_df.columns.tolist():
            columns[column_name] = scaled_df.get(column_name).values

        xaxis_label = self.get_xaxis_label(interval_type)

        level_dict = {'times': dts,
                      'locations': position_list,
                      'columns': columns,
                      'xaxis_label': xaxis_label
                      }

        return level_dict

    def get_xaxis_label(self, interval_type):
        if(interval_type == 'days'):
            return 'Month/Days'
        elif(interval_type == 'hours'):
            return 'Day/Hours'
        elif (interval_type == 'minutes'):
            return 'Hour/Minutes'
        else:
            return 'Minute/Seconds'