import unittest
from molecule_parser import MoleculeParser

class MoleculeParserTest(unittest.TestCase):

    def test_parse_molecule_with_empty_formula(self):
        result = MoleculeParser.parse_molecule("")
        expectedResult = {}
        self.assertDictEqual(result, expectedResult)

    def test_parse_molecule_with_no_submolecules(self):
        water = "H2O"
        result = MoleculeParser.parse_molecule(water)
        expectedResult = {"H" : 2, "O" : 1}
        self.assertDictEqual(result, expectedResult)

    def test_parse_molecule_with_one_submolecule(self):
        magnesiumHydroxide = "Mg(OH)2"
        result = MoleculeParser.parse_molecule(magnesiumHydroxide)
        expectedResult = {"Mg": 1, "O": 2, "H": 2}
        self.assertDictEqual(result, expectedResult)