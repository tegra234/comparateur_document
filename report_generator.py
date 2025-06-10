def generate_line_summary(diff_result):
    """
    Génère un résumé clair à partir des résultats de comparaison ligne par ligne.
    :param diff_result: dictionnaire contenant les résultats de la comparaison
    :return: string formaté
    """
    lines = []
    lines.append(f"Lignes identiques : {len(diff_result['identical'])}")
    lines.append(f"Lignes seulement dans fichier 1 : {len(diff_result['only_in_1'])}")
    lines.append(f"Lignes seulement dans fichier 2 : {len(diff_result['only_in_2'])}")
    lines.append(f"Lignes différentes totales : {len(diff_result['different'])}")
    return '\n'.join(lines)

def format_diff_output(diff_raw):
    """
    Formate les lignes avec indicateurs de différence (+ pour ajout, - pour suppression).
    :param diff_raw: liste brute de diffs (difflib.ndiff)
    :return: string formaté
    """
    return '\n'.join(diff_raw)

def format_word_differences(word_diffs):
    """
    Formate les différences mot à mot ligne par ligne.
    :param word_diffs: liste de dicts contenant les diffs mot à mot
    :return: string formaté
    """
    lines = []
    for diff in word_diffs:
        lines.append(f"Ligne {diff['line_number']}:")
        lines.append(f"  - Fichier 1: {diff['line1']}")
        lines.append(f"  - Fichier 2: {diff['line2']}")
        for tag, i1, i2, j1, j2 in diff['word_diff']:
            if tag != 'equal':
                lines.append(f"    * {tag.upper()} : {' '.join(diff['line1'].split()[i1:i2])} -> {' '.join(diff['line2'].split()[j1:j2])}")
    return '\n'.join(lines)

def format_similarity_report(similarity, word_count1, word_count2, unique1, unique2):
    """
    Formate le résumé de similarité entre deux fichiers.
    :param similarity: pourcentage de similarité
    :param word_count1: nombre de mots dans le fichier 1
    :param word_count2: nombre de mots dans le fichier 2
    :param unique1: mots uniques à fichier 1
    :param unique2: mots uniques à fichier 2
    :return: string formaté
    """
    lines = []
    lines.append(f"Taux de similarité : {similarity} %")
    lines.append(f"Nombre total de mots dans fichier 1 : {word_count1}")
    lines.append(f"Nombre total de mots dans fichier 2 : {word_count2}")
    lines.append(f"Mots présents seulement dans fichier 1 ({len(unique1)}) : {', '.join(sorted(unique1))}")
    lines.append(f"Mots présents seulement dans fichier 2 ({len(unique2)}) : {', '.join(sorted(unique2))}")
    return '\n'.join(lines)

def format_keyword_search(keyword, freq1, freq2):
    """
    Affiche la fréquence d'un mot-clé dans les deux fichiers.
    :param keyword: mot-clé à chercher
    :param freq1: fréquence dans fichier 1
    :param freq2: fréquence dans fichier 2
    :return: string formaté
    """
    return f"Mot-clé '{keyword}' trouvé {freq1} fois dans le fichier 1, {freq2} fois dans le fichier 2."

def export_report(filename, report_text):
    """
    Sauvegarde le rapport dans un fichier texte.
    :param filename: nom du fichier de sortie
    :param report_text: contenu du rapport à sauvegarder
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(report_text)
    except IOError as e:
        print(f"Erreur lors de la sauvegarde du rapport : {e}")
