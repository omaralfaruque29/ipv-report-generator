import matplotlib.pyplot as plt
from utils import get_ticks, get_resource_dir


class TableGenerator:
    def generate(self):
        raise NotImplementedError("must be implemented")

class RegularTable (TableGenerator):

    def generate(self, dataframe):
        try:
            fig, axs = plt.subplots(1, 1)
            col_label = ['Date']
            cell_list = []
            colors = ['gray']

            ticks = get_ticks()
            locations = ticks['locations']
            df = dataframe.iloc[locations, ]

            for timestamp in df.index:
                time = []
                time.append(str(timestamp).split('+')[0])
                cell_list.append(time)

            for col in df.columns.tolist():
                col_label.append(str(col))
                colors.append('gray')
                i = 0
                for value in df[str(col)]:
                    cell_list[i].append(value)
                    i = i +1

            axs.axis('off')
            axs.table(cellText=cell_list, colLabels=col_label, loc='center', colColours=colors)
            plt.title('Regular Table')
            resource_dir = get_resource_dir()
            plt.savefig(resource_dir + '/table.png')
            # plt.show()

        except Exception as e:
            print('error from regular table class: ', e)


class StatTable(TableGenerator):

    def generate(self, dataframe):
        try:
            plt.subplots(1, 1)
            col_label = ['Date']
            cell_list = []
            colors = ['gray']

            ticks = get_ticks()
            location_list = ticks['locations']
            df = dataframe.iloc[location_list, ]

            for i in range(len(df.index) - 1):
                row = []
                row.append(str(df.index[i]).split("+")[0] + '-->' + str(df.index[i + 1]).split("+")[0])
                cell_list.append(row)

            totals = []
            for col_name in dataframe.columns.tolist():
                col_label.append(str(col_name))
                col_label.append(str(col_name) + '_percentage')
                colors.append('gray')
                colors.append('gray')
                column = dataframe[str(col_name)].values
                total = sum(column)
                totals.append(total)
                for i in range(len(cell_list)):
                     interval_summation = sum(column[location_list[i]:location_list[i+1]])
                     cell_list[i].append(interval_summation)
                     cell_list[i].append('%.2f' % ((interval_summation / float(total)) * 100))
            last_row = ['Total']
            for ttl in totals:
                last_row.append(ttl)
                last_row.append(100)
            cell_list.append(last_row)

            plt.figure(figsize=(11, 7))
            plt.table(cellText=cell_list, colLabels=col_label, loc='center', colColours=colors)
            plt.title('Stat Table')
            plt.axis('off')
            resource_dir = get_resource_dir()
            # plt.show()
            plt.savefig(resource_dir + '/stat_table.png')

        except Exception as e:
            print('error from stattable class: ', e)

class ManagementTable(TableGenerator):

    def generate(self, data):
        try:
            measurement = data.columns[0]
            dataframe = data.drop(columns = measurement)
            col_label = dataframe.columns.values.tolist()
            cell_list = []
            colors = ['orange' for i in range(len(col_label))]

            for index, row in dataframe.iterrows():
                tbl_row = []
                for i, v in row.items():
                    tbl_row.append(v)
                cell_list.append(tbl_row)

            fig, axs = plt.subplots(1, 1)
            axs.axis('off')
            axs.table(cellText=cell_list, colLabels=col_label, loc='center', colColours=colors)
            plt.title(str(measurement).upper() + ' usage')
            resource_dir = get_resource_dir()
            plt.savefig(resource_dir + '/' + measurement + '.png')
            # plt.show()

        except Exception as e:
            print('error from management table class: ', e)




class NoTable (TableGenerator):
    def generate(self, data):
        pass

class TableGeneratorFactory:
    def create_generator(self, type):
        if type == "Regular":
            return RegularTable()
        elif type == 'StatTable':
            return StatTable()
        elif type == 'Management':
            return ManagementTable()
        else:
            return NoTable()