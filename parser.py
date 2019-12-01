import re
from html.parser import HTMLParser

class Document():
    def __init__(self, name, t):
        self.name = name
        self.type = t

        self.text = ""
        self.sents = []

        self.before_sents = []
        self.after_sents = []
        self.during_sents = []

    def append(self, text):
        self.text += text.replace("\n", " ")

    def process_text(self):
        # print(self.text)
        buffer = re.split(r"(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s", self.text)

        self.sents = []
        for sent in buffer:
            if len(sent) == 0:
                continue
            split = re.split(r"(?<!\w\.\w.)(?<![A-Z][a-z])(?<=\.\"|\?\")\s", sent)
            if split:
                self.sents += split
            else:
                self.sents.append(sent)

        for sent in self.sents:
            if " after " in sent:
                self.after_sents.append(sent)
            if "before" in sent:
                self.before_sents.append(sent)
            if "during" in sent:
                self.during_sents.append(sent)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

class Parser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.total_line_count = 0
        self.after_line_count = 0
        self.before_line_count = 0
        self.during_line_count = 0

        self.current_doc = None
        self.docs = []

        self.current_tag = None

    def handle_starttag(self, tag, attrs):
        # print(tag)
        if tag == "doc":
            if self.current_doc:
                self.current_doc.process_text()
                self.docs.append(self.current_doc)
            doc = Document(attrs[0][1], attrs[1][1])
            self.current_doc = doc
        if tag == "headline":
            self.current_tag = "headline"
            # print("headline")
        if tag == "dateline":
            self.current_tag = "dateline"
            # print("dateline")
        if tag == "text":
            self.current_tag = "text"
            # print("text")


    def handle_data(self, data):
        # print(data)
        if not data or data.isspace():
            return
        if self.current_tag == "text":
            self.total_line_count += 1
            self.current_doc.append(data)
            if "after" in data:
                self.after_line_count += 1
            if "before" in data:
                self.before_line_count += 1
            if "during" in data:
                self.during_line_count += 1
