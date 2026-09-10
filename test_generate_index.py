import os
import tempfile
import unittest

from generate_index import generate_index


class GenerateIndexTest(unittest.TestCase):
    def test_file_links_are_url_encoded(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            old_cwd = os.getcwd()
            try:
                os.chdir(temp_dir)
                with open('example report.html', 'w', encoding='utf-8') as f:
                    f.write('ok')
                with open('workbook.xlsx', 'w', encoding='utf-8') as f:
                    f.write('ok')

                generate_index()

                with open('index.html', 'r', encoding='utf-8') as f:
                    content = f.read()

                self.assertIn('href="example%20report.html"', content)
                self.assertNotIn('href="example report.html"', content)
                self.assertIn('href="workbook.xlsx"', content)
            finally:
                os.chdir(old_cwd)


if __name__ == '__main__':
    unittest.main()
