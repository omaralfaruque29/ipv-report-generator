from observer import Observer
from observer import Subject

class DataProcessor (Observer,Subject):
    report_generators = []

    def register_report_generator(self, generator):
        try:
            if generator not in self.report_generators:
                self.report_generators.append(generator)
                generator.register_subject(self)
            else:
                raise ValueError
        except ValueError:
            print "ERROR: generator already subscribe to Subject"
            raise ValueError


    def remove_report_generator(self, generator):
        try:
            if generator in self.report_generators:
                generator.remove_subject()
                self.report_generators.remove(generator)
            else:
                raise ValueError
        except ValueError:
            print "Error: generator currently not subscribed to Subject"
            raise ValueError

    def update_report_generators(self, request):
        for generator in self.report_generators:
            generator.update(self.processed_data, request)

class AnomolyDetector (DataProcessor):

    def update(self,request):
        self.data = self.subject.data
        self.notify(request)


    def processData(self, data, request):
        # TODO
        # process data
        return data

    def notify(self, request):
        self.processed_data = self.processData(self.data, request)
        self.update_report_generators(request)

class NoProcessing (DataProcessor):

    def update(self, request):
        self.data = self.subject.data
        self.notify(request)

    def processData(self, data, request):
        # TODO
        # process data
        return data

    def notify(self, request):
        self.processed_data = self.data
        self.update_report_generators(request)