import unittest

from apiaryProject import main


class TestProcessesMethods(unittest.TestCase):

    def setUp(self):
        self.page = main.handle_get("https://apiary.docs.apiary.io")
        # self.post = main.handle_post("https://api.apiary.io/blueprint/publish/publicpersonalapi",
        #                             "myFile.json")
        # self.error_content = '{"error":1,"message":"This resource requires authenticated API call."}'

    def test_get_page_return_code(self):
        self.assertEqual(self.page.status_code, 200)

    # def test_post_page_return_code(self):
        # self.assertEqual(self.post.status_code, 404)

    # def test_post_page_content(self):
        # self.assertEqual(self.post.content, self.error_content)

    def tearDown(self):
        # empty list (not to keep in memory)
        self.page = None
        self.post = None


if __name__ == '__main__':
    unittest.main()
