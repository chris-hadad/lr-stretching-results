"""Complete-roster refusal regressions for the actual example checker."""

import copy
import json
from pathlib import Path
import unittest
import reproduce_examples as example


class ExampleRosterTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = json.loads((Path(__file__).with_name("examples.json")).read_text())

    def refused(self, change):
        data = copy.deepcopy(self.source)
        change(data)
        with self.assertRaises((ValueError, KeyError, TypeError, IndexError)):
            example.verify_examples(data)

    def test_complete_source(self):
        self.assertEqual(
            example.verify_examples(self.source), {"families": 11, "directions": 2}
        )

    def test_missing_and_duplicated_populations(self):
        self.refused(lambda x: x.update(families=[], directions=[]))
        self.refused(lambda x: x["families"].pop())
        self.refused(
            lambda x: x["families"].__setitem__(1, copy.deepcopy(x["families"][0]))
        )
        self.refused(lambda x: x["directions"].pop())
        self.refused(
            lambda x: x["directions"].__setitem__(1, copy.deepcopy(x["directions"][0]))
        )

    def test_missing_and_duplicated_count_grades(self):
        self.refused(lambda x: x["families"][0]["count_sites"].pop())
        self.refused(
            lambda x: x["families"][0]["count_sites"].__setitem__(
                1, copy.deepcopy(x["families"][0]["count_sites"][0])
            )
        )
        self.refused(lambda x: x["directions"][0]["independent_parent_counts"].pop())
        self.refused(
            lambda x: x["directions"][1]["independent_parent_counts"].__setitem__(
                1, copy.deepcopy(x["directions"][1]["independent_parent_counts"][0])
            )
        )
        self.refused(
            lambda x: x["directions"][0]["independent_parent_counts"][0]["checks"].pop()
        )
        self.refused(lambda x: x["families"][0]["unused_check_grades"].pop())

    def test_changed_frozen_parameters_and_values(self):
        self.refused(lambda x: x["families"][0]["w"].__setitem__(0, 3))
        self.refused(lambda x: x["families"][0].__setitem__("prior_degree", 0))
        self.refused(lambda x: x["directions"][0].__setitem__("S", 0))
        self.refused(
            lambda x: x["families"][0]["count_sites"][0].__setitem__("count", 0)
        )
        self.refused(lambda x: x["families"][0]["literal_LR"].pop())
        self.refused(lambda x: x["families"][0]["triple"][0].__setitem__(0, 32))


if __name__ == "__main__":
    unittest.main()
