import re


def normalize_text(text, to_lower=True, remove_punctuation=True, normalize_spaces=True):
    """
    Nettoie et normalise un texte selon les options spécifiées.
    :param text: Texte d'entrée
    :param to_lower: Convertir en minuscules
    :param remove_punctuation: Supprimer la ponctuation
    :param normalize_spaces: Normaliser les espaces multiples
    :return: Texte nettoyé
    """
    if to_lower:
        text = text.lower()

    if remove_punctuation:
        text = re.sub(r'[\p{P}\p{S}]', '', text, flags=re.UNICODE)  # Peut échouer selon l'interpréteur
        text = re.sub(r'[\.,;:!?"()\[\]{}<>\-]', '', text)

    if normalize_spaces:
        text = re.sub(r'\s+', ' ', text)

    return text.strip()


def preprocess_lines(lines, mode='souple'):
    """
    Prétraite une liste de lignes selon le mode.
    :param lines: Liste de lignes de texte
    :param mode: 'strict' ou 'souple'
    :return: Liste de lignes prétraitées
    """
    if mode not in ['strict', 'souple']:
        raise ValueError("Mode de prétraitement invalide. Utilisez 'strict' ou 'souple'.")

    cleaned_lines = []
    for line in lines:
        if mode == 'strict':
            cleaned_lines.append(line.strip())
        else:  # mode == 'souple'
            cleaned = normalize_text(
                line,
                to_lower=True,
                remove_punctuation=True,
                normalize_spaces=True
            )
            cleaned_lines.append(cleaned)
    return cleaned_lines


def count_words(lines):
    """
    Compte le nombre total de mots dans une liste de lignes.
    :param lines: Liste de lignes de texte
    :return: Entier (nombre total de mots)
    """
    return sum(len(line.strip().split()) for line in lines)
