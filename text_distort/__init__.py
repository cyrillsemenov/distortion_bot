import random
import sys
from typing import Dict, List, Optional

import re

import requests


def reduplicate(word: str, repl: str = "ху", soften: bool = True) -> str:
    """
    Introduce reduplication in a Russian word.
    """
    # prefixes = ["при", "до", "без"]
    prefixes = [
        "без", "вдоль", "вне", "вслед",
        "вы", "между", "мимо", "на", "над", "надо", "об", "от", "по", "под",
        "после", "пред", "при", "с", "сверх", "среди", "средь", "через"
    ]

    softening = {
        "а": "я",
        "о": "ё",
        "у": "ю",
        "ы": "и",
        "э": "е",
    }

    # Check if the word starts with a prefix
    prefix = ""
    for p in prefixes:
        if word.startswith(p):
            prefix = prefix+word[:len(p)]
            word = word[len(p):]

    # stoplist = ["хуй", "хуе", "хуё", ]
    # if any([word.startswith(s) for s in stoplist]):
    #     return prefix + word

    pattern = re.search(r"[^аоуыэяёюие]+", word)
    if pattern:
        prefix = prefix+word[:pattern.start()]
        word = word[pattern.start()+1:]

    # Soften first vowel after replacement
    if soften and any([word.startswith(s) for s in "аоуыэ"]):
        word = re.sub(r"[аоуыэ]", lambda x: softening[x.group()], word, count=1)

    # Concatenate prefix, sub and word
    return prefix + repl + word


def cut_suffix(word):
    suffix = ''
    if len(word) == 0:
        return word, suffix, False

    if word[-1] in ['.', ',', '?', '!']:
        suffix = word[-1]
    return word.lower().strip(' ,.?!'), suffix, word.istitle()


def levenshtein_distance(str1, str2):
    len_str1 = len(str1)
    len_str2 = len(str2)
    distance_matrix = [[0 for _ in range(len_str2 + 1)] for _ in range(len_str1 + 1)]
    for i in range(len_str1 + 1):
        for j in range(len_str2 + 1):
            substitution_cost = int(str1[i - 1] != str2[j - 1])
            distance_matrix[i][j] = min(distance_matrix[i - 1][j] + 1,
                                        distance_matrix[i][j - 1] + 1,
                                        distance_matrix[i - 1][j - 1] + substitution_cost)
    return distance_matrix[len_str1][len_str2]


class TextDistort:
    def __init__(self,
                 db_path: str, gist_id: Optional[str] = None, substring_length: int = 2
                 ):
        """
        This class creates a text distortion effect by using a given dictionary file as a reference.
        It compares words in the text to be distorted with the words in the dictionary file,
        and if there is a match within a specified Levenshtein distance threshold,
        it substitutes the word in the text with a similar word from the dictionary.
        The class utilizes a substring matching technique
        to optimize the search process and minimize the computation time.

        :param db_path: path to text file with list of words
        :param gist_id: optional id of a gist with data,
            if provided `db_path` must be the name of the file in the gist
        :param substring_length: length of the substrings that are taken
            from the beginning and end of each word when the database is created
        """
        self.database: Dict[tuple, List[str]] = {}
        self._db_path = db_path
        self._gist_id = gist_id
        # self._threshold = threshold
        self._g = substring_length
        # self._rp = reduplication_probability
        self._load_data()

    def __call__(
            self,
            string: str, threshold: int = 6, reduplication_probability: float = 0.2,
            *args, **kwargs
    ) -> str:
        """
        Mock words

        :param string: input string to be distorted
        :param threshold: maximal Levenshtein distance to substitute words
        :param reduplication_probability: if the word is not in the list,
            the probability of its echo-duplication
        :return: distorted string
        """
        words = [self._lookup(word, threshold, reduplication_probability) for word in string.split()]
        return " ".join(words).strip()

    def _populate(self, word):
        word = word.strip()
        first_chars = word[0:self._g]
        last_chars = word[-self._g:]
        if self.database.get((first_chars, last_chars)):
            self.database[(first_chars, last_chars)].append(word)
        else:
            self.database[(first_chars, last_chars)] = [word, ]

    def _load_data(self) -> None:
        if self._gist_id:
            r = requests.get(f"https://api.github.com/gists/{self._gist_id}")
            lines = r.json()['files'][self._db_path]['content'].splitlines()
            for line in lines:
                self._populate(line)
        elif self._db_path:
            with open(self._db_path) as fd:
                for line in fd.readlines():
                    self._populate(line)

    def _lookup(self, word_raw: str, threshold: int, reduplication_probability: float) -> str:
        word, suffix, is_title = cut_suffix(word_raw)
        first_chars, last_chars = word[0:self._g], word[-self._g:]
        res = word

        if len(word) < 4:
            pass
        elif not (first_chars, last_chars) in self.database:
            stoplist = ["хуй", "хуе", "хуё", "хуя"]
            if not any([word.startswith(s) for s in stoplist]) and random.random() < reduplication_probability:
                res = reduplicate(word, repl="ху", soften=True)
        elif threshold > 0:
            candidates = [
                word for word in self.database[(first_chars, last_chars)]
                if levenshtein_distance(word, word) < threshold
            ]
            if candidates:
                res = random.choice(candidates)
        else:
            candidates = [
                word for word in self.database[(first_chars, last_chars)]
            ]
            res = sorted(candidates, key=lambda x: levenshtein_distance(x, word))[0]
        if is_title:
            res = res.title()
        return res + suffix


if __name__ == "__main__":
    distort = TextDistort(db_path='explicit_words_list.txt')
    for in_line in sys.stdin:
        if in_line:
            print(distort(in_line))
        else:
            print("")
