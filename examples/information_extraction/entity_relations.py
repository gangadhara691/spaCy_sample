#!/usr/bin/env python
# coding: utf8
"""A simple example of extracting relations between phrases and entities using
spaCy's named entity recognizer and the dependency parse. Here, we extract
money and currency values (entities labelled as MONEY) and then check the
dependency tree to find the noun phrase they are referring to – for example:
$9.4 million --> Net income.

Compatible with: spaCy v2.0.0+
"""
from __future__ import unicode_literals, print_function
from sample001 import convertMultiple
import plac
import spacy
fname="ar_2013_e.pdf.txt"
pdfDir = "C:/Users/ssadanal/Desktop/python-spacy/pdf2txt/pdf/"
txtDir = "C:/Users/ssadanal/Desktop/python-spacy/pdf2txt/txt/"
#convertMultiple(pdfDir, txtDir)

#with open(txtDir + fname, encoding="utf8") as f:
#    content = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
#content = [x.strip() for x in content]

TEXTS = ['''Leveraged finance comprises infrastructure finance, essential services and other types of finance. It excludes investment grade financing and
non-investment grade financing where there is no private equity sponsor involvement. This definition is subject to refinement moving forward. As
at October 31, 2013, our total commitments, combined funded and unfunded of $13.6 billion, increased $1.5 billion from the prior year,
reflecting an increase in client volumes. As at October 31, 2013, our total commitments, combined funded and unfunded represented 1.6% of
our total assets similar to the prior year.''']
#content

@plac.annotations(
    model=("Model to load (needs parser and NER)", "positional", None, str))
def main(model='en_core_web_sm'):
    nlp = spacy.load(model)
    print("Loaded model '%s'" % model)
    print("Processing %d texts" % len(TEXTS))

    for text in TEXTS:
        doc = nlp(text)
        relations = extract_currency_relations(doc)
        for r1, r2 in relations:
            print('{:<10}\t{}\t{}'.format(r1.text, r2.ent_type_, r2.text))


def extract_currency_relations(doc):
    # merge entities and noun chunks into one token
    spans = list(doc.ents) + list(doc.noun_chunks)
    for span in spans:
        span.merge()

    relations = []
    for money in filter(lambda w: w.ent_type_ == 'MONEY', doc):
        if money.dep_ in ('attr', 'dobj'):
            subject = [w for w in money.head.lefts if w.dep_ == 'nsubj']
            if subject:
                subject = subject[0]
                relations.append((subject, money))
        elif money.dep_ == 'pobj' and money.head.dep_ == 'prep':
            relations.append((money.head.head, money))
    return relations


if __name__ == '__main__':
    plac.call(main)

    # Expected output:
    # Net income      MONEY   $9.4 million
    # the prior year  MONEY   $2.7 million
    # Revenue         MONEY   twelve billion dollars
    # a loss          MONEY   1b
