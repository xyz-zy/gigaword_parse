from nltk.parse.corenlp  import CoreNLPParser
from distant import Example, get_relation
from nltk import Tree, ParentedTree

SOURCE = "afp_eng_199406"
LABEL = "after"
FILE = SOURCE + "_" + LABEL + ".txt"
TMP_PATH = "./" + LABEL + "_tmp/"
failed_event_parse = 0

INPUT_FILE = SOURCE + "_" + LABEL + ".txt"
OUTPUT_FILE = "examples/" + SOURCE + "_" + LABEL + ".json"

def main():
    parser = CoreNLPParser(url='http://localhost:9000')

    total_sents = 0
    num_examples = 0
    output_file = open(OUTPUT_FILE, "w")
    print("[", file=output_file)

    with open(INPUT_FILE) as input_file:
        for line in input_file:
            total_sents += 1
            # print(line)
            parse = next(parser.raw_parse(line))
            # print(parse)
            tree = ParentedTree.fromstring(parse.__str__())
            example = get_relation(input_file, tree)

            if example:
                if num_examples > 0:
                    print(",", file=output_file)
                print(example.to_json(), file=output_file)
                num_examples += 1

    print("]", file=output_file)

    print("total after sentences: ", total_sents)
    print("examples parsed: ", num_examples)


if __name__ == "__main__":
    main()
