import unittest
import filehandlers
import textwrap
import os


class Tests(unittest.TestCase):
    def setUp(self):
        self.af = filehandlers.AbstractFile("test.txt")
        self.m = filehandlers.FileManipulator(self.af)
        self.af.touch()

    def tearDown(self):
        self.m.delete()

    def test_file_naming(self):
        self.assertEqual(str(self.af), "test.txt")

    def test_file_exists(self):
        self.assertTrue(self.af.exists())

    def test_writing_to_files(self):
        self.assertTrue(self.af.exists())
        b = self.af.wrap()
        self.assertEqual(b.read(), "")
        b.close()  # to fix resourcewarning
        self.assertEqual(self.m.get_cache(), [])
        self.m.write_to_file("cool\nthings")
        self.m.refresh()
        self.assertEqual(self.m.get_cache(), ["cool", "things"])
        self.assertEqual(
            self.m.get_file_contents_singlestring(),
            textwrap.dedent(
                """\
                    cool
                    things"""  # noqa
            )  # noqa
        )

    @unittest.skipUnless(os.getenv("CIRRUS_CI") is not None, reason="not CI")
    def test_abspath(self):
        self.assertEqual(abs(self.af), "/tmp/cirrus-ci-build/test.txt")

    def test_semistrict_types(self):
        with self.assertRaises(TypeError):
            filehandlers.FileManipulator(0)  # wrong type on purpose


if __name__ == "__main__":
    unittest.main()
