class texteditor:
    def __init__(self, filename):
        self.text = []
        self.history = []
        self.modificated = False
        self.filename = filename
        self.clipboard = ""

        try:
            with open(filename, "r") as file:
                self.text = file.readlines()
        except FileNotFoundError:
            self.text = []

    def insert(self, text, row=None, col=None):
        if row == None:
            self.text.append(text)
        else:
            row = int(row)
            while len(self.text) <= row:
                self.text.append("")
