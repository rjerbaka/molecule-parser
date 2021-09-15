import unittest

class MoleculeParserTest(unittest.TestCase):

    def test_parse_molecule(self):
        moleculeParser = MoleculeParser()
        result = moleculeParser.parse_molecule("")
        expected_result = {}
        self.assertDictEqual(result, expected_result)