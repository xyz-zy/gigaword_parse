import argparse
import gzip
from parser import Parser


BATCH_SIZE = 2000
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

def filter_file(filename, source, doc):
    parser = Parser()
    with gzip.open(filename + ".gz", "rt") as file:
        for line in file:
            parser.feed(line)

    total_sent_count = 0
    after_sent_count = 0
    before_sent_count = 0
    during_sent_count = 0

    for doc in parser.docs:
        total_sent_count += len(doc.sents)


    after_sents = set()
    before_sents = set()
    during_sents = set()
    for doc in parser.docs:
        after_sents.update(doc.after_sents)
        before_sents.update(doc.before_sents)
        during_sents.update(doc.during_sents)
    after_sents = list(after_sents)
    before_sents = list(before_sents)
    during_sents = list(during_sents)

    write("filtered/" + SOURCE + "_" + DOC + "_after", after_sents)
    write("filtered/" + SOURCE + "_" + DOC + "_before", before_sents)
    write("filtered/" + SOURCE + "_" + DOC + "_during", during_sents)


    print("File ", filename)
    print("total sent count: ", total_sent_count)
    print("after sent count: ", len(after_sents))
    print("before sent count: ", len(before_sents))
    print("during sent count: ", len(during_sents))

parser = argparse.ArgumentParser()
parser.add_argument('--dir', help='path to gigaword/data/')
parser.add_argument('--source', nargs="?", help='afp_eng,apw_eng,cna_eng,ltw_eng,nyt_eng,wpb_eng,xin_eng')
parser.add_argument('--date', nargs="+", help='YYYYMM')
args = parser.parse_args()


DATA_DIR = args.dir if args.dir else "../gigaword_eng_5/data/"
SOURCE = args.source

for date in args.date:
    DOC = date
    FILE = DATA_DIR + SOURCE + "/"  + SOURCE + "_" + DOC

    filter_file(FILE, SOURCE, DOC)
