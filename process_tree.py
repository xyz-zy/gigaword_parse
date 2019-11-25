import glob
import os

from distant import Example, get_relation
from nltk import Tree, ParentedTree

PATH = "filtered/"


def process_tree(tree_str, label):
    # print(tree_str)

    tree = ParentedTree.fromstring(tree_str.__str__())
    example = get_relation(tree, label)

    return example


def get_next_tree(file):
    tree = ""
    line = file.readline()

    while not line.isspace() and len(line) > 0:
        tree += line
        line = file.readline()

    return tree

def get_label(filename):
    if "after" in filename:
        return "after"
    elif "before" in filename:
        return "before"
    elif "during" in filename:
        return "during"
    return None

def process_trees(filename):
    num_examples = 0
    label = get_label(filename)

    output_filename = "examples/" + filename[len("filtered/"):-5] + ".json"
    if os.path.exists(output_filename):
        return
    output_file = open(output_filename, "w")
    print("[", file=output_file)

    with open(filename) as file:

        tree = get_next_tree(file)

        while len(tree) > 0:
            # print(tree)
            example = process_tree(tree, label)

            if example:
                if num_examples > 0:
                    print(",\n" + example.to_json(), file=output_file, end="")
                else:
                    print(example.to_json(), file=output_file, end="")

                num_examples += 1
            else:
                print("error")

            tree = get_next_tree(file)

    print("\n]", file=output_file)


def main():

    for filename in glob.glob(PATH + "*.tree"):
        print(filename)
        process_trees(filename)


if __name__ == "__main__":
    main()


