from random import uniform
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
from pandas import DataFrame
from sklearn.linear_model import LinearRegression

from contracts import contract, new_contract
from utility import DateTimeInterval
from utils import get_ticks, get_resource_dir

class GraphGenerator:

    def generate(self):
        raise NotImplementedError("must be implemented")

    @new_contract
    def is_dataframe(self, dataframe):
        if not isinstance(dataframe, DataFrame):
           raise ValueError("Arguemnt %s is not a DataFrame" % dataframe)
        pass

    @contract
    def get_values(self, dataframe):
        '''
        this function splits dataframe object into a columnar dictionary
        :param: dataframe
        :type dataframe: is_dataframe
        :rtype: dict[>0]
        '''
        columns = {}
        for i in range(len(dataframe.columns)):
            column_name = dataframe.columns[i]
            column_values = dataframe[column_name].tolist()
            columns[column_name] = column_values
        return columns


    @contract
    def get_level(self, dataframe):
        '''
        this function returns all time stamps as a list from dataframe object
        :param: dataframe
        :type dataframe: is_dataframe
        :rtype: list[>0]
        '''
        levels = []
        for d in dataframe.index.tolist():
            levels.append(str(d))
        return levels


    def get_random_color(self):
        '''
        return a tuple for generating rgb random color
        '''
        return (uniform(0.1, 0.9), uniform(0.1, 0.9), uniform(0.1, 0.9), uniform(0.1, 0.9))


class LineChartGenerator(GraphGenerator):


    def trend(self, data):
        '''
        generate trend line of all columns in the given dataframe  and save into resource directory
        :param: data
        :type data: is_dataframe
        '''
        try:
            X = range(len(data))
            X = np.reshape(X, (len(X), 1))
            for col_name in data.columns:
                y = data[col_name].tolist()
                model = LinearRegression()
                model.fit(X, y)
                trend = model.predict(X)
                xticks = get_ticks()
                level = self.get_level(data)
                plt.clf()
                fig = plt.figure(figsize=(11, 7))
                ax = fig.add_subplot(1, 1, 1)
                ax.plot(level, y)
                ax.plot(level, trend)
                ax.set_xticks(xticks['locations'])
                ax.set_xticklabels(xticks['times'], rotation=30, fontsize='small')
                ax.set_title(col_name + '_trend')
                ax.set_xlabel(xticks['xaxis_label'])
                ax.legend(loc='best')
                ax.grid(linestyle='solid', linewidth=1, alpha=0.3)
                img_dir = get_resource_dir()
                plt.savefig(img_dir + '/' + col_name + '.png')

        except Exception as e:
            print('error from trend:', e)


    def generate(self, data):
        '''
        generate line chart and save into resource directory
        :param: data
        :type data: is_dataframe
        '''
        self.trend(data)
        try:
            level = self.get_level(data)
            xticks = get_ticks()
            columns = self.get_values(data)
            ylbl = ''
            opacity = 1
            fig = plt.figure(figsize=(11, 7))
            ax = fig.add_subplot(1, 1, 1)

            for k, v in columns.items():
                column_name = k.capitalize()
                column_values = v
                ylbl = ylbl + '_' + column_name
                color = self.get_random_color()
                ax.plot(level, column_values, label=column_name, color=color, alpha=opacity, drawstyle='steps-post')

            ax.set_xticks(xticks['locations'])
            ax.set_xticklabels(xticks['times'], rotation=30, fontsize='small')
            ax.legend(loc='best')
            ax.grid(linestyle='solid', linewidth=1, alpha=0.3)
            ax.set_title(ylbl[1:] + ' Vs Time')
            ax.set_xlabel(xticks['xaxis_label'])
            ax.set_ylabel(ylbl[1:])
            img_dir = get_resource_dir()
            plt.savefig(img_dir + '/line.png')
            # plt.show()

        except Exception as e:
            print('error from line chart: ', e)

class BarChartGenerator (GraphGenerator):

    def generate(self, data):
        '''
        generate bar chart and save into resource directory
        :param: data
        :type data: is_dataframe
        '''
        try:
            xticks = get_ticks()
            columns = xticks['columns']
            xaxis_groups = np.arange(len(columns.itervalues().next()))
            index = xaxis_groups
            bar_width = 0.35
            opacity = 1
            ylbl = ''
            plt.figure(figsize=(11, 7))
            plt.ylim(DateTimeInterval.ymin, DateTimeInterval.ymax)
            for k,v in columns.items():
                column_name = k.capitalize()
                column_values = v
                ylbl = ylbl + '_' + column_name
                color = self.get_random_color()
                plt.bar(index, column_values, bar_width,
                                alpha=opacity,
                                color=color,
                                align='center',
                                label=column_name)
                index = index + bar_width

            plt.grid(linestyle='solid', linewidth=1, alpha=0.3)
            plt.xlabel(xticks['xaxis_label'])
            plt.ylabel(ylbl[1:])
            plt.title(ylbl[1:] + ' Vs Time')
            plt.xticks(xaxis_groups, xticks['times'])
            plt.legend()
            img_dir = get_resource_dir()
            plt.savefig(img_dir + '/bar.png')
            # plt.show()

        except Exception as e:
            print('error from bar chart: ', e)


class PieChartGenerator (GraphGenerator):

    def generate(self, data):
        '''
        generate pie chart and save into resource directory
        :param: data
        :type data: is_dataframe
        '''
        try:
            columns = self.get_values(data)
            slices = []
            activities = []
            colors = []
            ylbl = ''
            plt.figure(figsize=(11, 7))
            for k, v in columns.items():
                column_name = k
                column_values = v
                activities.append(column_name)
                slices.append(sum(column_values))
                ylbl = ylbl + '_' + column_name
                colors.append(self.get_random_color())

            plt.figure(figsize=(11, 7))

            plt.pie(slices,
                    labels=activities,
                    colors=colors,
                    startangle=180,
                    autopct='%1.2f')

            plt.title(ylbl[1:])
            img_dir = get_resource_dir()
            plt.savefig(img_dir + '/pie.png')
            # plt.show()

        except Exception as e:
            print('error from pie chart: ', e)


class NoChart (GraphGenerator):
    def generate(self, data):
        pass

class GraphGeneratorFactory:
    def create_generator(self, type):
        if type == "Pie":
            return PieChartGenerator()
        elif type == "Bar":
            return BarChartGenerator()
        elif type == "Line":
            return LineChartGenerator()
        else:
            return NoChart()