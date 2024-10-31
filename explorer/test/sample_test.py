import unittest
import Explorer

class ExploreFunctionTest(unittest.TestCase):
    def test_txt_files(self):
        expected_result = {'testmedia/a': 1, 'testmedia/a/dir': 1}
        actual_result = Explorer.explore("txt", "test_media")
        self.assertEqual(actual_result, expected_result,
                         f"\nخروجی تابع برای پسوند txt و پوشه‌ی testmedia باید برابر باشد با:\n{expected_result}\nاما دریافت شد:\n{actual_result}")

    def test_mkv_files(self):
        """تست شمارش فایل‌های mkv در پوشه testmedia"""
        expected_result = {'testmedia/a/a/b': 1}
        actual_result = Explorer.explore("mkv", "testmedia")
        self.assertEqual(actual_result, expected_result,
                         f"\nخروجی تابع برای پسوند mkv و پوشه‌ی testmedia باید برابر باشد با:\n{expected_result}\nاما دریافت شد:\n{actual_result}")

if __name__ == "__main__":
    unittest.main()
