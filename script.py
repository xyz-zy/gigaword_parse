import gzip
from parser import Parser

DATA_DIR = "../gigaword_eng_5/data/"
SOURCE = "nyt_eng"
DOC = "199409"
FILE = DATA_DIR + SOURCE + "/"  + SOURCE + "_" + DOC


parser = Parser()
with gzip.open(FILE+".gz", "rt") as file:
    for line in file:
        parser.feed(line)

total_sent_count = 0
after_sent_count = 0
before_sent_count = 0
during_sent_count = 0

for doc in parser.docs:
    total_sent_count += len(doc.sents)
    after_sent_count += len(doc.after_sents)
    before_sent_count += len(doc.before_sents)
    during_sent_count += len(doc.during_sents)

print("total sent count: ", total_sent_count)
print("after sent count: ", after_sent_count)
print("before sent count: ", before_sent_count)
print("during sent count: ", during_sent_count)

BATCH_SIZE = 3000
def write(out_filename, sents):
    it = 0
    beg = 0
    end = min(len(sents), BATCH_SIZE)

    while beg < len(sents):
        with open(out_filename + "_" + str(it) + ".txt", "w") as out_file:
            for i in range(beg, end):
                out_file.write(sents[i] + "\n")

        beg = end
        end = min(len(sents), beg + BATCH_SIZE)
        it += 1


after_sents = []
before_sents = []
during_sents = []
for doc in parser.docs:
    after_sents.extend(doc.after_sents)
    before_sents.extend(doc.before_sents)
    during_sents.extend(doc.during_sents)

write("filtered/" + SOURCE + "_" + DOC + "_after", after_sents)
write("filtered/" + SOURCE + "_" + DOC + "_before", before_sents)
write("filtered/" + SOURCE + "_" + DOC + "_during", during_sents)
