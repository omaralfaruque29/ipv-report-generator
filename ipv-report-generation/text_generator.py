class TextGenerator:
    def generate(self):
        raise NotImplementedError("must be implemented")

class Summary (TextGenerator):
    def generate(self, data):
        pass

class Detail (TextGenerator):
    def generate(self, data):
        pass

class NoText (TextGenerator):
    def generate(self, data):
        pass

class TextGeneratorFactory:
    def create_generator(self, type):
        if type == "summary":
            return Summary()
        elif type == "detail":
            return Detail()
        else:
            return NoText()