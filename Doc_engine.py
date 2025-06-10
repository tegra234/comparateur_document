import difflib
from collections import Counter

def compare_lines(lines1, lines2):
    """
    Compare deux listes de lignes et retourne les différences.
    :param lines1: Lignes du fichier 1
    :param lines2: Lignes du fichier 2
    :return: Dictionnaire des différences et des similitudes
    """
    diff = list(difflib.ndiff(lines1, lines2))
    identical = []
    only_in_1 = []
    only_in_2 = []
    different = []

    for line in diff:
        if line.startswith('  '):
            identical.append(line[2:])
        elif line.startswith('- '):
            only_in_1.append(line[2:])
        elif line.startswith('+ '):
            only_in_2.append(line[2:])

    # Lignes différentes = celles uniquement présentes dans l'un ou l'autre
    different = only_in_1 + only_in_2

    return {
        'identical': identical,
        'only_in_1': only_in_1,
        'only_in_2': only_in_2,
        'different': different,
        'diff_raw': diff
    }

def compare_words_in_lines(lines1, lines2):
    """
    Compare les lignes mot par mot.
    :param lines1: Lignes du fichier 1
    :param lines2: Lignes du fichier 2
    :return: Liste de différences mot à mot
    """
    comparisons = []
    for i, (l1, l2) in enumerate(zip(lines1, lines2)):
        if l1 != l2:
            sm = difflib.SequenceMatcher(None, l1.split(), l2.split())
            word_diff = list(sm.get_opcodes())
            comparisons.append({
                'line_number': i + 1,
                'line1': l1,
                'line2': l2,
                'word_diff': word_diff
            })
    return comparisons

def calculate_similarity(lines1, lines2):
    """
    Calcule un taux de similarité basé sur les lignes.
    :param lines1: Lignes du fichier 1
    :param lines2: Lignes du fichier 2
    :return: Pourcentage de ressemblance
    """
    matcher = difflib.SequenceMatcher(None, lines1, lines2)
    return round(matcher.ratio() * 100, 2)

def unique_words(text1, text2):
    """
    Identifie les mots uniques à chaque texte.
    :param text1: Texte 1 (str)
    :param text2: Texte 2 (str)
    :return: Tuple (set1 - set2, set2 - set1)
    """
    words1 = set(text1.split())
    words2 = set(text2.split())
    return words1 - words2, words2 - words1

def word_frequencies(text):
    """
    Calcule les fréquences de chaque mot dans un texte.
    :param text: Texte brut
    :return: Counter des mots
    """
    return Counter(text.split())
