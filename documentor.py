#_d Generates documentation from annotations
#_d Clemens Tiedt
#_d February 2018

class Documentor:

    def __init__(self, path):
        """Creates a documentation from docstrings and comments"""
        self.requirements = []
        self.doctext = ""
        self.doctext_tex = ""
        with open(path) as file:
            self.lines = file.readlines()
        #_d This function returns None

    def parse(self):
        """Translates the input file into documentation"""
        #_d Go through all lines
        for i, line in enumerate(self.lines):
            indent_level = len(line) - len(line.strip()) - 1
            #_d Check for imports
            if line.strip().startswith("import"):
                for el in line.strip()[7:].split(", "):
                    self.requirements.append(el)
            if line.strip().startswith("from"):
                self.requirements.append(line.strip().split(" ")[1])
            #_d Check for class declarations
            if line.strip().startswith("class"):
                self.doctext += " " * indent_level + "Class " + line.strip()[6:-1] + "\n"
            #_d Check for function declarations
            if line.strip().startswith("def"):
                self.doctext += " " * indent_level + "Function " + line.strip()[4:-1] + "\n"
            #_d Check for docstrings
            if line.strip().startswith('"""'):
                if line.strip().endswith('"""'):
                    self.doctext += " " * indent_level + line.strip()[3:-3] + "\n"
                #_d If a docstring is multiline, search for the end
                else:
                    self.doctext += " " * indent_level + line.strip()[3:] + "\n"
                    k = 1
                    while not self.lines[i+k].strip().endswith('"""'):
                        self.doctext += " " * indent_level + self.lines[i+k].strip() + "\n"
                        k += 1
                    self.doctext += self.lines[i + k][:-3]  + "\n"
            #_d Search for comments marked as relevant
            if "#_d" in line and '"#_d"' not in line:
                self.doctext += " " * indent_level + line[line.index("#_d")+4:]
            if line.strip() == "":
                self.doctext += "\n"
            #_d After all lines have been processed, add the imports to the documentation text
        self.doctext = "Requires " + ", ".join(self.requirements) + "\n" + self.doctext
        #_d This function returns None

    def save(self, path):
        """Saves the documentation to the specified path"""
        with open(path) as file:
            file.write(self.doctext)
        #_d This function returns None
            
