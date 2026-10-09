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

    def test_nested_folders_reports(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            old_cwd = os.getcwd()
            try:
                os.chdir(temp_dir)
                prod_mini_dir = os.path.join('Prod', 'Mini')
                os.makedirs(prod_mini_dir)
                with open(os.path.join(prod_mini_dir, 'sample mini.html'), 'w', encoding='utf-8') as f:
                    f.write('ok')
                with open(os.path.join(prod_mini_dir, 'sample mini.xlsx'), 'w', encoding='utf-8') as f:
                    f.write('ok')

                generate_index()

                with open('index.html', 'r', encoding='utf-8') as f:
                    content = f.read()

                self.assertIn('href="Prod/Mini/sample%20mini.html"', content)
                self.assertIn('href="Prod/Mini/sample%20mini.xlsx"', content)
                self.assertIn('Prod &bull; Mini', content)
                self.assertIn('Mini', content)
            finally:
                os.chdir(old_cwd)


if __name__ == '__main__':
    unittest.main()
