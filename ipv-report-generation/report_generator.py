import os

import graph_generator, table_generator, text_generator
from observer import Observer
from os import listdir
from fpdf import FPDF

class ReportGenerator(Observer):

    graph_gen_factory = graph_generator.GraphGeneratorFactory()
    table_gen_factory = table_generator.TableGeneratorFactory()
    text_gen_factory = text_generator.TextGeneratorFactory()

    def generate_report(self):
        raise NotImplementedError("must be implemented")

    def get_chart(self, _charts, data):
        for chart in _charts:
            data_chart = self.graph_gen_factory.create_generator(chart)
            data_chart.generate(data)


    def get_table(self, _table, data):
        for table in _table:
            data_table =  self.table_gen_factory.create_generator(table)
            data_table.generate(data)

    def get_text(self, _text,data):
        for txt in _text:
            data_text = self.table_gen_factory.create_generator(txt)
            data_text.generate(data)


class PDFGenerator (ReportGenerator):

    def update(self, data, request):
        self.generate_report(data, request)

    def generate_report(self, data, request):
        self.get_chart(request['visualization_type']['Chart'], data)
        self.get_table(request['visualization_type']['Table'], data)
        self.get_pdf_file()
        self.get_text(request['visualization_type']['Text'], data)


    def get_pdf_file(self):
        '''
        collect all charts, tables from resource directory and combine them into a single pdf file called report.pdf
        '''
        project_dir = os.path.abspath('main.py').split('main.py')[0]
        resource_dir = project_dir + 'resources'
        pdf = FPDF()
        for image_file in listdir(resource_dir):
            print(image_file)
            pdf.add_page()
            pdf.image(resource_dir + '/' + image_file, 0, 50, 210, 150)
        pdf.output(name='report.pdf', dest='F')



class DocGenerator (ReportGenerator):
    def update(self,request):
        print self.data
        # graph_gen = self.graph_gen_factory.create_generator(request.graph_type)
        # table_gen = self.table_gen_factory.create_generator(request.table_type)
        text_gen = self.text_gen_factory.create_generator("summary")


    def generate_report(self):
        pass