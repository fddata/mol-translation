import pandas as pd
import re


def _parse_formula(formula):
    parts = re.findall(r'([A-Z][a-z]?)(\d*)', formula)
    return {
        element: int(count) if count else 1
        for element, count in parts
    }


def _get_atom_count_per_molecule(formula: str, atom: str) -> int:
    parts = _parse_formula(formula)
    return parts.get(atom, 0)



def get_inchi_strings_for_atom(atom: str, target_count: int) -> list[str]:
    """
    returns a list of inchis containing the combined total of target atoms
    e.g. atom=C, count=100 will return random inchis that contain a total of
    at least 100 carbons.  Used to generate a list to pass to the main draw
    functions to generate training images.
    """

    df_train_labels = pd.read_csv("../../data/train_labels.csv", nrows=100)

    df_formula = df_train_labels["InChI"].str.split("/", n=2, expand=True)[1]

    print(df_formula)

    running_total = 0

    TO_DO
    while running_total < target_count:
        pick an index at random
        if the target atom is no zero, add it to a list, increment running_total
        if it is zero
    

if __name__ == "__main__":
    # get_inchi_strings_for_atom(atom='C', count=50)
    print(_get_atom_count_per_molecule("C13H15BrN2O3", "X"))