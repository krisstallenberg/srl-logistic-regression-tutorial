def extract_predicate(sentence):
    for word in sentence:
        if word['predicate'] != '_':
            return [word['predicate'] for _ in sentence]

def extract_predicate_lemma(sentence):
    for word in sentence:
        if word['predicate'] != '_':
            return [word['lemma'] for _ in sentence]