#!/bin/bash

cd ../stanford-corenlp-full-2018-02-27/

for filename in ../gigaword_parse/filtered/${1}*.txt; do
  name=${filename##*/}
  base=${name%.txt}
  echo $base
  java -mx2000m edu/stanford/nlp/parser/lexparser/LexicalizedParser -outputFormat "penn" -maxLength 100 edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz $filename > ../gigaword_parse/tree/${base}.tree
done

