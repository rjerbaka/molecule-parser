from re import findall as find_all_regex_matches

class MoleculeParser:
    
    
    SUB_MOLECULE_REGEX = r"([([{])([a-zA-Z]*)([\])}])(\d*)"

    #enclosures = {"{": "}", "[": "]", "(": ")"}

    #atomRegex = compile_regex(ATOM_REGEX)
    #subMoleculeRegex = compile_regex(SUB_MOLECULE_REGEX)
    

    def parse_molecule(moleculeFormula):
        """

        """

        moleculeComposition = {}

        moleculeComposition =  MoleculeParser.parse_simple_molecule(moleculeFormula, 1)

        return moleculeComposition


    def parse_simple_molecule(moleculeFormula, moleculeFactor):
        """

        """

        ATOM_REGEX = r"([A-Z][a-z]{0,2})(\d*)"
        atomList = find_all_regex_matches(ATOM_REGEX, moleculeFormula)
        moleculeComposition = MoleculeParser.get_molecule_composition_from_matched_atom_list(atomList, moleculeFactor)
        
        return moleculeComposition


    def get_molecule_composition_from_matched_atom_list(regexMatchedAtomList, moleculeFactor):
        """

        """

        moleculeComposition = {}

        for matchedAtom in regexMatchedAtomList:
            matchedAtomSymbol = matchedAtom[0]
            matchedAtomFactor = MoleculeParser.calculate_atom_factor_in_molecule(matchedAtom[1], moleculeFactor) 
            moleculeComposition[matchedAtomSymbol] = matchedAtomFactor

        return moleculeComposition



    def calculate_atom_factor_in_molecule(matchedFactor, moleculeFactor):
        """

        """

        atomFactor = MoleculeParser.get_atom_factor_from_regex_match(matchedFactor)

        return atomFactor * moleculeFactor


    def get_atom_factor_from_regex_match(matchedFactor):
        """

        """

        matchedAtomFactor = 1
        matchedAtomHasAFactor = len(matchedFactor) > 0
        
        if matchedAtomHasAFactor :
            matchedAtomFactor = int(matchedFactor)

        return matchedAtomFactor

        
