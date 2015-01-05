
import nltk

from nltk.tree import Tree
from django.conf import settings
from nltk.tag.stanford import NERTagger
from nltk.parse.stanford import StanfordParser

##########################################################################
## JAR loading
##########################################################################

def create_tagger(model=None, jar=None, encoding='ASCII'):
    model = model or settings.STANFORD_NER_MODEL
    jar   = jar or settings.STANFORD_NER_JAR

    return NERTagger(model, jar, encoding)

def create_parser(models=None, jar=None, **kwargs):
    models = models or settings.STANFORD_PARSER_MODELS
    jar   = jar or settings.STANFORD_PARSER_JAR

    return StanfordParser(jar, models, **kwargs)

##########################################################################
## Stateful tagging/parsing
##########################################################################

class NER(object):

    tagger = None

    @classmethod
    def initialize_tagger(klass, model=None, jar=None, encoding='ASCII'):
        klass.tagger = create_tagger(model, jar, encoding)

    @classmethod
    def tag(klass, sent):
        if klass.tagger is None:
            klass.initialize_tagger()

        sent = nltk.word_tokenize(sent)
        return klass.tagger.tag(sent)

class Parser(object):

    parser = None

    @classmethod
    def initialize_parser(klass, models=None, jar=None, **kwargs):
        klass.parser = create_parser(models, jar, **kwargs)

    @classmethod
    def parse(klass, sent):
        if klass.parser is  None:
            klass.initialize_parser()

        return klass.parser.raw_parse(sent)

##########################################################################
## Helper functions to class objects
##########################################################################

def tag(sent):
    return NER.tag(sent)

def parse(sent):
    return Parser.parse(sent)

##########################################################################
## Phrase extraction
##########################################################################

def entities(sent):

    def extract(tags, idx, jdx):
        # print "%i -- %i" % (idx, jdx)
        term = " ".join([word for word, _ in tags[idx:jdx]])
        return term, tags[idx][1]

    def window(tags):
        idx  = 0
        for jdx in xrange(len(tags)):
            if tags[jdx][1] != tags[idx][1]:
                # Discovered mismatch between tag at JDX and IDX
                yield extract(tags, idx, jdx)
                idx = jdx # Set the new positions

        # Don't forget the last one (to the end)
        yield extract(tags, idx, None)

    tags = tag(sent)
    for term, nec in window(tags):
        if nec != "O":
            yield {
                'term': term,
                'tag': nec,
            }

def contains_subclause(tree):
    for child in tree:
        if isinstance(child, Tree) and child.label().startswith('S'):
            return True
    return False

def extract_phrases(tree, phrase):
    if phrase in tree.label() and not contains_subclause(tree):
        yield tree.copy(True)
    else:
        for child in tree:
            if isinstance(child, Tree):
                for subtree in extract_phrases(child, phrase):
                    yield subtree.copy(True)

def extract_noun_phrases(tree):
    for phrase in extract_phrases(tree, 'NP'):
        words = phrase.pos()
        for tag in ('DT', 'WP', 'PRP', 'IN'):
            if tag in words[0][1]:
                words = words[1:]
                break

        if len(words) > 0:
            yield " ".join([word for word,tag in words])
