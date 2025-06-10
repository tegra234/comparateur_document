
import difflib
from collections import Counter


def compare_lines(lines1, lines2):
    """
    Compare deux listes de lignes et retourne les lignes communes, différentes et uniques.
    :param lines1: lignes du fichier 1
    :param lines2: lignes du fichier 2
    :return: (communes, différentes, uniques_1, uniques_2)
    """
    set1, set2 = set(lines1), set(lines2)
    common = list(set1 & set2)
    diff = list((set1 ^ set2))
    unique1 = list(set1 - set2)
    unique2 = list(set2 - set1)
    return common, diff, unique1, unique2


def compare_words_in_lines(lines1, lines2):
    """
    Compare ligne par ligne, mot à mot, si le nombre de lignes est égal.
    :param lines1: lignes du fichier 1
    :param lines2: lignes du fichier 2
    :return: liste des différences mot à mot
    """
    differences = []
    for idx, (l1, l2) in enumerate(zip(lines1, lines2)):
        if l1 != l2:
            sm = difflib.SequenceMatcher(None, l1, l2)
            diff_detail = [f"{tag} '{l1[i1:i2]}' -> '{l2[j1:j2]}" for tag, i1, i2, j1, j2 in sm.get_opcodes() if tag != 'equal']
            differences.append((idx, diff_detail))
    return differences


def calculate_similarity(lines1, lines2):
    """
    Calcule un taux de similarité entre deux listes de lignes.
    :return: pourcentage de similarité (float)
    """
    sm = difflib.SequenceMatcher(None, '\n'.join(lines1), '\n'.join(lines2))
    return round(sm.ratio() * 100, 2)


def unique_words(lines):
    """
    Retourne un ensemble de mots uniques dans un document.
    :param lines: liste de lignes de texte
    :return: set de mots
    """
    words = set()
    for line in lines:
        words.update(line.strip().split())
    return words


def word_frequencies(lines):
    """
    Calcule la fréquence de chaque mot dans une liste de lignes.
    :param lines: liste de lignes de texte
    :return: Counter des mots
    """
    words = []
    for line in lines:
        words.extend(line.strip().split())
    return Counter(words)
