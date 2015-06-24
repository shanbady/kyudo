# fugato.similarity
# Implements the similarity comparison for case reasoning.
#
# Author:   Benjamin Bengfort <bengfort@cs.umd.edu>
# Created:  Tue Jun 23 20:19:33 2015 -0400
#
# Copyright (C) 2015 University of Maryland
# For license information, see LICENSE.txt
#
# ID: similarity.py [] benjamin@bengfort.com $

"""
Implements the similarity comparison for case reasoning.
"""

##########################################################################
# Imports
##########################################################################

import os
import json

from itertools import combinations
from nltk import wordpunct_tokenize
from nltk.stem import WordNetLemmatizer
from kyudo.utils import Timer, memoized
from freebase.nlp import parse, extract_phrases

##########################################################################
# Case Representation
##########################################################################


class QuestionCase(object):
    """
    Data structure for holding a case for similarity analytics. Right now
    this is coupled to the front end and is not the final case representation.
    """

    lemmatizer = WordNetLemmatizer()

    def __init__(self, question, answer, subgoals=None, **options):
        """
        Text should be the raw text of the question that is going to be
        parsed and analyzed. Answer can be a string or it can be a freebase
        topic. Suboals can be related QuestionCases or similar objects.
        """
        self.question = question
        self.answer = answer
        self.subgoals = subgoals
        self.options = options

    @memoized
    def lemmas(self):
        """
        Returns the lemmas from the Question text.
        """
        return set([
            self.lemmatizer.lemmatize(token).lower()
            for token in wordpunct_tokenize(self.question)
        ])

    @memoized
    def parse(self):
        """
        Returns the parse of the question text. Memoizes for quick access.
        """
        return parse(self.question)

    @memoized
    def noun_phrases(self):
        """
        Returns all the noun phrases from the question text.
        """
        if self.parse:
            return set([
                " ".join(np.leaves()) for np
                in extract_phrases(self.parse[0], 'NP')
            ])

##########################################################################
# Similarity Class
##########################################################################


class Similarity(object):
    """
    Performs similarity analytics on a set of cases.
    """

    def __init__(self, cases):
        """
        Cases are expected to be (question, answer) pairs where both the
        question and the answer are raw text. Currently the question is
        parsed and scored, while the
        """
        self.cases = [
            QuestionCase(*case) for case in cases
        ]

    def entities(self):
        """
        Returns all the entities from the cases.
        """
        for case in self:
            for np in case.noun_phrases:
                yield np

    def jaccard(self):
        """
        Returns the pairwise Jaccard scores.
        """
        for a,b in combinations(self.cases, 2):
            a = a.lemmas
            b = b.lemmas
            yield float(len(a & b)) / float(len(a | b))

    def group_jaccard(self):
        scores = list(self.jaccard())
        return sum(scores) / float(len(scores))

    def __getitem__(self, idx):
        return self.cases[idx]

    def __iter__(self):
        for case in self.cases:
            yield case

##########################################################################
# Case Fixtures
##########################################################################


class CaseFixture(object):
    """
    Memoized fixture for loading cases from disk.
    """

    FIXTURES = os.path.join(os.path.dirname(__file__), "fixtures")

    def __init__(self, name):
        """
        Constructs a path using the JSON file and the fixtures directory.
        """
        self.path = os.path.join(self.FIXTURES, name)

    @memoized
    def fixtures(self):
        with open(self.path, 'r') as f:
            return json.load(f)

    def values(self):
        return self.fixtures.values()

    def dump(self):
        with open(self.path, 'w') as f:
            json.dump(self.fixtures, f, indent=4)

    def __getitem__(self, key):
        return self.fixtures[key]

    def __setitem__(self, key, value):
        self.fixtures[key] = value

    def __contains__(self, key):
        return key in self.fixtures

preselected_cases = CaseFixture("preselected_cases.json")
