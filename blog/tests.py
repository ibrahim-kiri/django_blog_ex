from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from .models import Post

# Create your tests here.
class BlogTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="admin", email="", password="admin"
        )

        cls.post = Post.objects.create(
            title = "News in Python",
            body="Python has been a great programming language in building AI , software development and data science",
            author=cls.user,
        )

    def test_post_model(self):
        self.assertEqual(self.post.title, "News in Python")
        self.assertEqual(self.post.body, "Python has been a great programming language in building AI , software development and data science")
        self.assertEqual(self.post.author.username, "admin")
        self.assertEqual(str(self.post), "News in Python")
        self.assertEqual(self.post.get_absolute_url(), "/post/1/")

    def test_url_exists_at_correct_location_listview(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_url_exists_at_correct_location_detailview(self):
        response = self.client.get("/post/1/")
        self.assertEqual(response.status_code, 200)

    def test_post_listview(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Python has been a great programming language in building AI , software development and data science")
        self.assertTemplateUsed(response, "home.html")

    def test_post_detailview(self):
        response = self.client.get(reverse("post_detail", kwargs={"pk": self.post.pk}))
        no_response = self.client.get("/post/100000/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, "News in Python")
        self.assertTemplateUsed(response, "post_detail.html")

    def test_post_createview(self):
        response = self.client.post(
                reverse("post_new"),
                {
                    "title": "Machine Learning",
                    "body": "Linear regression and classification influence most of the AI models in this era",
                    "author": self.user.id,
                },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.last().title, "Machine Learning")
        self.assertEqual(Post.objects.last().body, "Linear regression and classification influence most of the AI models in this era")

    def test_post_updateview(self):
        response = self.client.post(
                reverse("post_edit", args="1"),
                {
                    "title": "AI/ML",
                    "body": "Linear regression and classification influence most of the AI/ML models in this era"
                },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.last().title, "AI/ML")
        self.assertEqual(Post.objects.last().body, "Linear regression and classification influence most of the AI/ML models in this era")

    def test_post_deleteview(self):
        response = self.client.post(reverse("post_delete", args="1"))
        self.assertEqual(response.status_code, 302)
