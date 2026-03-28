#!/usr/bin/env python3
"""
Génère le rapport HTML à partir du notebook d'analyse hôpital.

Usage :
  cd genere_rapport
  python generer.py

  python generer.py --notebook ../projet_hopital/notebooks/analyse_hospital.ipynb
  python generer.py --no-execute --out ./rapports
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Répertoire contenant ce script (genere_rapport/)
HERE = Path(__file__).resolve().parent
ROOT_DATAVIZ = HERE.parent

DEFAULT_NOTEBOOK = ROOT_DATAVIZ / "projet_hopital" / "notebooks" / "analyse_hospital.ipynb"
DEFAULT_OUT = HERE / "rapports"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Exporte le notebook d'analyse en HTML (rapport)."
    )
    parser.add_argument(
        "--notebook",
        type=Path,
        default=DEFAULT_NOTEBOOK,
        help="Chemin vers le fichier .ipynb",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=DEFAULT_OUT,
        help="Dossier de sortie pour le HTML",
    )
    parser.add_argument(
        "--no-execute",
        action="store_true",
        help="Ne pas réexécuter le notebook (utiliser les sorties déjà dans le fichier)",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=600,
        help="Timeout par cellule lors de l'exécution (secondes)",
    )
    parser.add_argument(
        "--kernel",
        default="python3",
        help="Nom du noyau Jupyter",
    )
    args = parser.parse_args()

    nb_path = args.notebook.resolve()
    if not nb_path.is_file():
        print(f"Notebook introuvable : {nb_path}", file=sys.stderr)
        return 1

    args.out.mkdir(parents=True, exist_ok=True)

    sys.path.insert(0, str(HERE))
    from notebook_to_rapport import notebook_to_html_plotly

    html_path = notebook_to_html_plotly(
        str(nb_path),
        output_directory=str(args.out.resolve()),
        execute=not args.no_execute,
        timeout=args.timeout,
        kernel_name=args.kernel,
    )
    print(f"Rapport généré : {html_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
