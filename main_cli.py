import argparse
from file_parser import parse_file
from text_preprocessor import preprocess_text
from comparison_engine import compare_documents, compare_words_in_lines
from report_generator import (
    generate_line_summary,
    format_diff_output,
    format_word_differences,
    format_similarity_report,
    format_keyword_search,
    export_report
)

def main():
    parser = argparse.ArgumentParser(description="Comparateur de documents .txt et .pdf")
    parser.add_argument("file1", help="Chemin du premier fichier")
    parser.add_argument("file2", help="Chemin du deuxième fichier")
    parser.add_argument("--mode", choices=["strict", "souple"], default="souple", help="Mode de comparaison")
    parser.add_argument("--ignore-case", action="store_true", help="Ignorer les différences de casse")
    parser.add_argument("--clean", action="store_true", help="Nettoyer le texte (ponctuation, espaces)")
    parser.add_argument("--motcle", help="Mot-clé à rechercher dans les documents")
    parser.add_argument("--rapport", default="rapport_comparaison.txt", help="Nom du fichier de rapport")

    args = parser.parse_args()

    try:
        text1 = parse_file(args.file1)
        text2 = parse_file(args.file2)
    except Exception as e:
        print(f"Erreur de lecture des fichiers : {e}")
        return

    # Prétraitement des textes en fonction des options de l'utilisateur
    preprocessed_text1 = preprocess_text(text1, mode=args.mode, ignore_case=args.ignore_case, clean=args.clean)
    preprocessed_text2 = preprocess_text(text2, mode=args.mode, ignore_case=args.ignore_case, clean=args.clean)

    lines1 = preprocessed_text1.splitlines()
    lines2 = preprocessed_text2.splitlines()

    diff_result, diff_raw = compare_documents(lines1, lines2)
    word_diffs = compare_words_in_lines(lines1, lines2)

    word_count1 = len(preprocessed_text1.split())
    word_count2 = len(preprocessed_text2.split())
    unique1 = set(preprocessed_text1.split()) - set(preprocessed_text2.split())
    unique2 = set(preprocessed_text2.split()) - set(preprocessed_text1.split())
    similarity = round((len(diff_result['identical']) / max(len(lines1), len(lines2))) * 100, 2) if max(len(lines1), len(lines2)) > 0 else 0.0

    rapport_lines = []
    rapport_lines.append(generate_line_summary(diff_result))
    rapport_lines.append("\nDétails des différences (lignes) :")
    rapport_lines.append(format_diff_output(diff_raw))
    rapport_lines.append("\nDifférences mot à mot :")
    rapport_lines.append(format_word_differences(word_diffs))
    rapport_lines.append("\nRésumé de similarité :")
    rapport_lines.append(format_similarity_report(similarity, word_count1, word_count2, unique1, unique2))

    if args.motcle:
        keyword = args.motcle.lower()
        freq1 = preprocessed_text1.lower().split().count(keyword)
        freq2 = preprocessed_text2.lower().split().count(keyword)
        rapport_lines.append("\nRecherche du mot-clé :")
        rapport_lines.append(format_keyword_search(args.motcle, freq1, freq2))

    final_report = '\n'.join(rapport_lines)
    print("\n--- Rapport de comparaison ---\n")
    print(final_report)

    export_report(args.rapport, final_report)
    print(f"\nRapport sauvegardé dans : {args.rapport}")

if __name__ == "__main__":
    main()
