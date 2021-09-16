import unittest
from molecule_parser import MoleculeParser
from re import compile as compile_regex

class MoleculeParserTest(unittest.TestCase):

    water = "H2O"
    magnesiumHydroxide = "Mg(OH)2"
    fremySalt = "K4[ON(SO3)2]2"
    simpleSubmoleculeDict = {"OH": 2}
    complexSubmoleculeDict = {"OH": 2, "H2O": 3, "N": 1}
    waterComposition = {"H" : 2, "O" : 1}

    def test_parse_molecule_with_empty_formula(self):
        result = MoleculeParser.parse_molecule("")
        expectedResult = {}
        self.assertDictEqual(result, expectedResult)

    def test_parse_molecule_with_no_submolecules(self):
        result = MoleculeParser.parse_molecule(self.water)
        expectedResult = {"H" : 2, "O" : 1}
        self.assertDictEqual(result, expectedResult)

    def test_parse_molecule_with_one_submolecule(self):
        result = MoleculeParser.parse_molecule(self.magnesiumHydroxide)
        expectedResult = {"Mg": 1, "O": 2, "H": 2}
        self.assertDictEqual(result, expectedResult)

    def test_parse_molecule_with_multiple_submolecules(self):
        result = MoleculeParser.parse_molecule(self.fremySalt)
        expectedResult = {"K": 4, "O": 14, "N": 2, "S": 4}
        self.assertDictEqual(result, expectedResult)

    def test_extract_submolecules_with_one_submolecule(self):
        result = MoleculeParser.extract_submolecules(self.magnesiumHydroxide)
        expectedResult = {"OH": 2}
        self.assertDictEqual(result, expectedResult)

    def test_remove_submolecules_from_formula(self):
        result = MoleculeParser.remove_submolecules_from_formula(self.magnesiumHydroxide)
        expectedResult = "Mg"
        self.assertEqual(result, expectedResult)

    def test_sum_submolecule_compositions_with_single_submolecule(self):
        result = MoleculeParser.sum_submolecule_compositions(self.simpleSubmoleculeDict)
        expectedResult = {"H" : 2, "O" : 2}
        self.assertDictEqual(result, expectedResult)

    def test_sum_submolecule_compositions_with_multiple_submolecules(self):
        result = MoleculeParser.sum_submolecule_compositions(self.complexSubmoleculeDict)
        expectedResult = {"H" : 8, "O" : 5, "N" : 1}
        self.assertDictEqual(result, expectedResult)

    def test_multiply_molecule_composition_by_factor(self):
        result = MoleculeParser.multiply_molecule_composition_by_factor(self.waterComposition, 2)
        expectedResult = {"H" : 4, "O" : 2}
        self.assertDictEqual(result, expectedResult)

    def test_parse_simple_molecule(self):
        result = MoleculeParser.parse_simple_molecule(self.water, 2)
        expectedResult = {"H" : 4, "O" : 2}
        self.assertDictEqual(result, expectedResult)

    def test_parse_submolecules(self):
        result = MoleculeParser.parse_submolecules(self.fremySalt)
        expectedResult = {"O": 14, "N": 2, "S": 4}
        self.assertDictEqual(result, expectedResult)

    def test_get_molecule_composition_from_matched_atom_list(self):
        result = MoleculeParser.get_molecule_composition_from_matched_atom_list([("H","2"), ("O", "")], 2)
        expectedResult = {"H" : 4, "O" : 2}
        self.assertDictEqual(result, expectedResult)

    def test_calculate_atom_factor_in_molecule_with_empty_matched_factor(self):
        result = MoleculeParser.calculate_atom_factor_in_molecule("", 2)
        expectedResult = 2
        self.assertEqual(result, expectedResult)

    def test_calculate_atom_factor_in_molecule_with_double_digit_matched_factor(self):
        result = MoleculeParser.calculate_atom_factor_in_molecule("12", 1)
        expectedResult = 12
        self.assertEqual(result, expectedResult)

    def test_get_factor_from_regex_match_with_empty_match(self):
        result = MoleculeParser.get_factor_from_regex_match("")
        expectedResult = 1
        self.assertEqual(result, expectedResult)

    def test_get_factor_from_regex_match(self):
        result = MoleculeParser.get_factor_from_regex_match("3")
        expectedResult = 3
        self.assertEqual(result, expectedResult)



