import unittest

from resume_polish import polish, polish_one


class TestPolish(unittest.TestCase):
    def test_replaces_weak_verb(self):
        out = polish_one("负责用户后台系统，性能提升了30%")
        self.assertTrue(out.startswith("主导"))
        self.assertIn("30%", out)

    def test_extracts_number(self):
        out = polish_one("做了登录模块，把响应时间降低500ms")
        self.assertIn("500ms", out)

    def test_suggests_metric_when_missing(self):
        out = polish_one("参与公司官网改版")
        self.assertIn("量化结果", out)

    def test_empty_line(self):
        self.assertEqual(polish_one("   "), "")

    def test_polish_batch(self):
        result = polish(["负责 A 系统，提升20%", "做了报表工具"])
        self.assertEqual(len(result), 2)
        self.assertTrue(result[0].startswith("主导"))


if __name__ == "__main__":
    unittest.main()
