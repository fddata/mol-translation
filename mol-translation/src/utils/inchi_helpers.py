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



def get_inchi_strings_for_atom(atom: str, target_count: int, df: pd.DataFrame) -> list[str]:
    """
    returns a list of inchis containing the combined total of target atoms
    e.g. atom=C, count=100 will return random inchis that contain a total of
    at least 100 carbons.  Used to generate a list to pass to the main draw
    functions to generate training images.
    """

    result = []
    running_total = 0


    while running_total < target_count:
        random_row = df.sample(n=1)
        random_formula = random_row["formula"].values[0]

        if not random_formula:
            continue

        atom_count = _get_atom_count_per_molecule(random_formula, atom)
        if atom_count == 0:
            continue

        running_total += atom_count
        result.append(random_row["InChI"].values[0])

    return result


if __name__ == "__main__":
    # get_inchi_strings_for_atom(atom='C', count=50)
    print(_get_atom_count_per_molecule("C13H15BrN2O3", "X"))