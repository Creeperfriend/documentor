#Generates documentation from annotations
#Clemens Tiedt
#February 2018

class Documentor:

    def __init__(self, path):
        """Creates a documentation from docstrings and comments"""
        self.doctext = ""
        self.doctext_tex = ""
        with open(path) as file:
            self.lines = file.readlines()

    def parse(self):
        for i, line in enumerate(self.lines):
            indent_level = len(line) - len(line.strip()) - 1
            if line.strip().startswith("import"):
                self.doctext += "Requires the libraries: " + line.strip()[7:]
                k = 1
                while self.lines[i+k].strip().startswith('import'):
                    self.doctext += " " + self.lines[i+k].strip()[7:]
                    k += 1
                self.doctext += "\n"
                line = self.lines[i+k]
            if line.strip().startswith("class"):
                self.doctext += " " * indent_level + "Class " + line.strip()[6:-1] + "\n"
            if line.strip().startswith("def"):
                self.doctext += " " * indent_level + "Function " + line.strip()[4:-1] + "\n"
            if line.strip().startswith('"""'):
                if line.strip().endswith('"""'):
                    self.doctext += " " * indent_level + line.strip()[3:-3] + "\n"
                else:
                    self.doctext += " " * indent_level + line.strip()[3:] + "\n"
                    k = 1
                    while not self.lines[i+k].strip().endswith('"""'):
                        self.doctext += " " * indent_level + self.lines[i+k].strip() + "\n"
                        k += 1
                    self.doctext += self.lines[i + k][:-3]  + "\n"
            if "#_d" in line:
                self.doctext += " " * indent_level + line[line.index("#_d")+4:]
            if line.strip() == "":
                self.doctext += "\n"

    def save(self, path):
        with open(path) as file:
            file.write(self.doctext)
                
                
