import glob
import itertools
import json

from distant import Example


# from data.timeml import TimeMLExample

# class TimeMLExample(object):
#     """
#     A single training/test example for the TimeML dataset.
#     """
#     def __init__(self, text, e1_pos, e2_pos, label):
#         self.text = text
#         self.e1_pos = e1_pos
#         self.e2_pos = e2_pos
#         self.str_label = label
#         self.int_label = None

#         self.sentences = None
#         self.e1_sentence_num = None
#         self.e1_sentence_pos= None
#         self.e2_sentence_num = None
#         self.e2_sentence_pos = None

#     def __str__(self):
#         return self.text + "\n" + str(self.e1_pos) + " " + str(self.e2_pos) + " " + self.str_label

def g_convert_examples_to_features(examples, tokenizer, max_seq_length,
                                 doc_stride, is_training, segment_ids=False):
    """Loads a data file into a list of InputFeatures."""

    unique_id = 1000000000

    features = []
                
    # Generates features from examples.
    for (example_index, example) in enumerate(examples):
        input_tokens = list(itertools.chain.from_iterable([tokenizer.tokenize(w) for w in example.tokens]))
        # input_tokens = tokenizer.tokenize(example.text)
        
        # Maximum number of tokens that an example may have. This is equal to 
        # the maximum token length less 3 tokens for [CLS], [SEP], [SEP].
        max_tokens_for_doc = max_seq_length - 3

        # Skips this example if it is too long.
        if len(input_tokens) > max_tokens_for_doc:
            unique_id += 1
            continue
 
        # Creates mappings from words in original text to tokens.
        tok_to_orig_index = []
        orig_to_tok_index = []
        all_doc_tokens = []
        for (i, word) in enumerate(example.tokens):
            orig_to_tok_index.append(len(all_doc_tokens)) 
            tokens = tokenizer.tokenize(word)
            for token in tokens:
                tok_to_orig_index.append(i)
                all_doc_tokens.append(token)

        # + 1 accounts for CLS token
        tok_e1_pos = orig_to_tok_index[example.e1_pos] + 1
        tok_e2_pos = orig_to_tok_index[example.e2_pos] + 1
       

        # The -3 accounts for [CLS], [SEP] and [SEP]
        segment = 0

        tokens = []
        segment_ids = []
        tokens.append("[CLS]")
        segment_ids.append(segment)
        for token in input_tokens:
            tokens.append(token)
            segment_ids.append(segment)
            if token == '[SEP]':
                segment += 1

        input_ids = tokenizer.convert_tokens_to_ids(tokens)

        # The mask has 1 for real tokens and 0 for padding tokens. Only real
        # tokens are attended to.
        input_mask = [1] * len(input_ids)
        # Zero-pads up to the sequence length.
        while len(input_ids) < max_seq_length:
            input_ids.append(0)
            input_mask.append(0)
            segment_ids.append(0)

        assert len(input_ids) == max_seq_length
        assert len(input_mask) == max_seq_length
        assert len(segment_ids) == max_seq_length
        assert tok_e1_pos < max_seq_length
        assert tok_e2_pos < max_seq_length
 
        features.append(
            InputFeatures(
                unique_id=unique_id,
                example_index=example_index,
                tokens=tokens,
                input_ids=input_ids,
                input_mask=input_mask,
                segment_ids=segment_ids,
                label=example.int_label,
                e1_position=tok_e1_pos,
                e2_position=tok_e2_pos
            )
        )
        unique_id += 1

    return features


def get_examples(EXAMPLE_DIR="examples/"):
    example_files = glob.glob(EXAMPLE_DIR + "*_before.json")
    exs = []

    for FILE in example_files:
        with open(FILE) as file:
            exs_list = json.load(file)

            for ex_json in exs_list:
                example = Example.from_json(ex_json)
                exs.append(example)
    return exs
