import unittest
import re
from . import matching

class MatchingTest(unittest.TestCase):

    def test_search_normalization(self):
        corpus_text = ""
        with open("matching/test/corpus.txt") as fp:
            for line in fp:
                corpus_text += line
        matcher = matching.Matcher("matching/test/corpus.txt")
        segments = matching.load_segments("matching/test/segments.json")
        positions = matcher.match(segments)
        matches = matcher.get_matches(positions)
        for m in matches:

            # perfect match is found depsite casing and punctuation
            self.assertEqual(m["ratio"], 1)

            # only whitespace can differ between reconstructed string and corpus text
            self.assertTrue(m["corpus_text"] in re.sub('\s+', ' ', corpus_text))

if __name__ == '__main__':
    unittest.main()
