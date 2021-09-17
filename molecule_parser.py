from re import findall as find_all_regex_matches
from re import compile as compile_regex
from collections import Counter

class MoleculeParser:
    

    def parse_molecule(moleculeFormula):
        """
        Takes a molecule chemical formula and returns a dictionary with the atoms it contains and their count. 
        """

        submoleculeComposition = MoleculeParser.parse_submolecules(moleculeFormula)
        moleculeFormulaWithoutSubmolecules = MoleculeParser.remove_submolecules_from_formula(moleculeFormula)
        restOfMoleculeComposition =  MoleculeParser.parse_simple_molecule(moleculeFormulaWithoutSubmolecules, 1)
        moleculeComposition = dict(Counter(submoleculeComposition) + Counter(restOfMoleculeComposition))

        return moleculeComposition


    def parse_submolecules(moleculeFormula):
        """
        Takes a molecule formula and returns the combined atom composition of all its submolecules. 
        """

        submolecules = MoleculeParser.extract_submolecules(moleculeFormula)
        extractedSubmoleculeComposition = MoleculeParser.sum_submolecule_compositions(submolecules)

        return extractedSubmoleculeComposition


    def extract_submolecules(moleculeFormula):
        """
        Takes a molecule formula and returns a dictionary of all first-level submolecules and their count. 
        First-level submolecules correspond to top level brackets, for example in K4[ON(SO3)2]2, 
        ON(SO3)2 is the only first level submolecule.

        The chosen regular expression tolerates mistakes in terms of bracket types. For instance, the
        molecule parser will be able to parse the following formula: Mg(OH]2.
        """

        SUBMOLECULE_REGULAR_EXPRESSION = r"[([{]([A-Za-z([{)\]}\d]*)[)\]}](\d*)"
        matchedSubmolecules = find_all_regex_matches(SUBMOLECULE_REGULAR_EXPRESSION, moleculeFormula)

        submolecules = {}

        for submolecule in matchedSubmolecules:
            submoleculeFormula = submolecule[0]
            submoleculeFactor = MoleculeParser.get_factor_from_regex_match(submolecule[1])
            submolecules[submoleculeFormula] = submoleculeFactor

        return submolecules


    def remove_submolecules_from_formula(moleculeFormula):
        """
        Removes submolecules, their brackets and their indexes from a given formula. 
        """

        SUBMOLECULE_REGULAR_EXPRESSION_WITHOUT_TUPLES = r"[([{][A-Za-z([{)\]}\d]*[)\]}]\d*"
        matchedSubmolecules = find_all_regex_matches(SUBMOLECULE_REGULAR_EXPRESSION_WITHOUT_TUPLES, moleculeFormula)

        for submoleculeFormula in matchedSubmolecules:
            moleculeFormula = moleculeFormula.replace(submoleculeFormula, "")

        return moleculeFormula


    def sum_submolecule_compositions(submolecules):
        """
        Takes a list of submolecules and their indexes, returns the combined atom composition of these submolecules.
        """

        finalComposition = {}

        for submoleculeFormula in submolecules:
            submoleculeComposition = MoleculeParser.parse_molecule(submoleculeFormula)
            submoleculeFactor = submolecules[submoleculeFormula]
            submoleculeComposition = MoleculeParser.multiply_molecule_composition_by_factor(submoleculeComposition, submoleculeFactor)
            finalComposition = dict(Counter(finalComposition)+Counter(submoleculeComposition))

        return finalComposition

        
    def multiply_molecule_composition_by_factor(moleculeComposition, factor):
        """
        Multiplies the count of each atom in the input dictionary by the given factor.
        """
        moleculeComposition.update((atom, atomNumber * factor) for atom, atomNumber in moleculeComposition.items())

        return moleculeComposition


    def parse_simple_molecule(moleculeFormula, moleculeFactor):
        """
        Takes a simple molecule formula (with no submolecules) and a factor, extracts each atom then 
        calulates its atom composition. 

        The chosen regular expression assumes that an element symbol can't have more than 3 letters with at least
        one in caps.
        """

        ATOM_REGULAR_EXPRESSION = r"([A-Z][a-z]{0,2})(\d*)"
        atomList = find_all_regex_matches(ATOM_REGULAR_EXPRESSION, moleculeFormula)
        moleculeComposition = MoleculeParser.get_molecule_composition_from_matched_atom_list(atomList, moleculeFactor)
        
        return moleculeComposition


    def get_molecule_composition_from_matched_atom_list(regexMatchedAtomList, moleculeFactor):
        """
        Takes a list of (atom, index) tuples and returns a dictionary with the final counts multiplied with the 
        general molecule factor.
        """

        moleculeComposition = {}

        for matchedAtom in regexMatchedAtomList:
            matchedAtomSymbol = matchedAtom[0]
            matchedAtomFactor = MoleculeParser.calculate_atom_factor_in_molecule(matchedAtom[1], moleculeFactor) 
            moleculeComposition[matchedAtomSymbol] = matchedAtomFactor

        return moleculeComposition


    def calculate_atom_factor_in_molecule(matchedFactor, moleculeFactor):
        """
        From a text atom index and an int molecule factor, returns the final count for the given atom.
        """

        atomFactor = MoleculeParser.get_factor_from_regex_match(matchedFactor)

        return atomFactor * moleculeFactor


    def get_factor_from_regex_match(matchedFactor):
        """
        Returns the found count for a given atom. If the matched factor is an empty string, then there's only one occurrency of the given atom. 
        Thus, the method returns 1.
        """

        factor = 1
        matchedItemHasAFactor = len(matchedFactor) > 0
        
        if matchedItemHasAFactor :
            factor = int(matchedFactor)

        return factor

        
