import unittest
import filehandlers
import textwrap


class Tests(unittest.TestCase):
    def setUp(self):
        self.f = filehandlers.File("test.txt")
        self.f.touch()

    def tearDown(self):
        self.f.delete()

    def test_file_naming(self):
        self.assertEqual(self.f.get_file_name(), "test.txt")

    def test_file_exists(self):
        self.assertTrue(self.f.exists())

    def test_writing_to_files(self):
        self.assertTrue(self.f.exists())
        b = self.f.wrap()
        self.assertEqual(b.read(), "")
        b.close()  # to fix resourcewarning
        self.assertEqual(self.f.get_cache(), [])
        self.f.write_to_file("cool\nthings")
        self.f.refresh()
        self.assertEqual(self.f.get_cache(), ["cool", "things"])
        self.assertEqual(
            self.f.get_file_contents_singlestring(),
            textwrap.dedent(
                """\
                    cool
                    things"""  # noqa
            )  # noqa
        )


if __name__ == "__main__":
    unittest.main()
