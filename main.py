import argparse
from flask import render_template
from flask import Flask
import sys

app = Flask(__name__)


@app.route('/')
def index():
    print('U can use this as a debagger', file=sys.stderr)
    sys.stdout.flush()
    combined = [[i, j] for i, j in zip(src, trg)]
    error_avg = sum(error_num)/len(src)

    return render_template(
        "index.html",
        combined=combined,
        error_avg=round(error_avg, 2)
    )


@app.route('/category', methods=["GET"])
def categorize():
    category = dict.fromkeys(
        ["ADJ", "ADJ:FORM", "ADV", "CONJ", "CONTR", "DET", "MORPH", "NOUN", "NOUN:INFL", "NOUN:NUM", "NOUN:POSS", "ORTH", "OTHER", "PART",
         "PREP", "PRON", "PUNCT", "SPELL", "UNK", "VERB", "VERB:FORM", "VERB:INFL", "VERB:SVA", "VERB:TENSE", "WO", "noop"], 0)
    for error in errors:
        code = error["code"]
        category[f"{code}"] = category[f"{code}"]+1

    key = [k for k, v in category.items()]
    value = [v for k, v in category.items()]

    cat = open("./error_description.txt", "r").read().split("\n\n")

    print(value, file=sys.stderr)
    return render_template(
        "category.html",
        key=key,
        value=value,
        error_categories=cat
    )


@app.route('/prefix', methods=["GET"])
def prefix():
    category = dict.fromkeys(
        ["Missing", "Replacement", "Unnecessary", "No Error"], 0)
    for error in errors:
        code = error["prefix"]
        category[f"{code}"] = category[f"{code}"]+1

    key = [k for k, v in category.items()]
    value = [v for k, v in category.items()]

    print(value, file=sys.stderr)
    return render_template(
        "prefix.html",
        key=key,
        value=value,
    )


def m2_to_sentences(m2):
    global src, trg, errors, error_num
    src, trg, errors, error_num = [], [], [], []
    skip = {"noop", "UNK", "Um"}

    for sent in m2:
        sent = sent.split("\n")
        orig = sent[0].split()[1:]  # Ignore "S "
        cor_sent = orig[:]
        edits = sent[1:]
        error_num.append(len(edits))
        offset = 0

        for edit in edits:
            edit = edit.split("|||")
            prefix, code, pos = error_category(edit)
            errors.append({"prefix": prefix, "code": code, "pos": pos})

            if edit[1] in skip:
                continue  # Ignore certain edits
            coder = int(edit[-1])
            # if coder != args.id:
            #     continue  # Ignore other coders

            span = edit[0].split()[1:]  # Ignore "A "
            start = int(span[0])
            end = int(span[1])
            cor = edit[2].split()

            plus, minus = "+++", "---"
            if prefix == "Replacement":  # if Replacement
                plus = minus = "???"
            cor = list(map(lambda s: code+plus+s, cor))
            for i in range(start, end):
                orig[i] = code+minus+orig[i]
            cor_sent[start + offset:end + offset] = cor
            offset = offset - (end - start) + len(cor)
        trg.append(" ".join(cor_sent))
        src.append(" ".join(orig))


def error_category(edit):
    prefix = "No Error"
    code = edit[1]
    if code[1] == ":":
        prefix = code[0]
        code = code[2:]
    if prefix == "M":
        prefix = "Missing"
    elif prefix == "R":
        prefix = "Replacement"
    elif prefix == "U":
        prefix = "Unnecessary"
    pos = code.split(":")[0]

    if pos == "noop":
        pos = "No Error"
    elif pos != "NOUN" and pos != "VERB" and pos != "ADJ" and pos != "ADV":
        pos = "OTHER"
    return prefix, code, pos


def main(args):
    m2_file = "./ABC.train.gold.bea19.m2"
    print(args.file_input)
    if args.file_input != None:
        m2_file = args.file_input
    m2 = open(m2_file, encoding="utf-8").read().strip().split("\n\n")
    m2_to_sentences(m2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--file_input", "-f", help="path to the m2 file")
    args = parser.parse_args()

    main(args)

    app.run()
