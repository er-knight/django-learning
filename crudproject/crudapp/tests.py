from json import dumps

from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone

from . import models

class BlogsViewTests(TestCase):

    client = Client()

    def test_get_request_when_blog_id_is_none(self):
        # print("--- test_get_request_when_blog_id_is_none ---")
        response = self.client.get(reverse("blogs"))
        self.assertEqual(response.status_code, 400)

    def test_get_request_when_blog_id_is_not_none_and_blog_exists(self):
        
        # print("--- test_get_request_when_blog_id_is_not_none_and_blog_exists ---")

        author = models.Author(
            name="test", email="test@example.com", summary="test author summary"
        )
        author.save()

        # print(list(models.Author.objects.all().values())) 

        blog = models.Blog(
            title="test blog", content="test blog content",
            author=author, pub_date=timezone.now()
        )
        blog.save()

        # print(list(models.Blog.objects.all().values()))        
        
        response = self.client.get(reverse("blogs_with_id", args=[blog.id]))
        self.assertEqual(response.status_code, 200)

    def test_get_request_when_blog_id_is_not_none_and_blog_not_exists(self):
        # print("--- test_get_request_when_blog_id_is_not_none_and_blog_not_exists ---")

        response = self.client.get(reverse("blogs_with_id", args=[1]))
        self.assertEqual(response.status_code, 404)

    def test_post_request_when_blog_id_is_not_none(self):
        # print("--- test_post_request_when_blog_id_is_not_none ---")
        
        response = self.client.post(reverse("blogs_with_id", args=[1]))
        self.assertEqual(response.status_code, 400)

    def test_post_request_when_blog_id_is_none_and_request_body_invalid(self):
        # print("--- test_post_request_when_blog_id_is_none_and_request_body_invalid ---")

        response = self.client.post(reverse("blogs"))
        self.assertEqual(response.status_code, 400)

    def test_post_add_new_blog_when_author_not_exists(self):

        # print("--- test_post_add_new_blog_when_author_not_exists ---")

        # print(list(models.Blog.objects.all().values()))        

        response = self.client.post(reverse("blogs"), data=dumps({
            "title": "test blog", "content": "tests blog content", "author": "test"
        }), content_type="json")
        self.assertEqual(response.status_code, 404)

        # print(list(models.Blog.objects.all().values()))        

    def test_post_add_new_blog_when_author_exists(self):

        # print("--- test_post_add_new_blog_when_author_exists ---")

        author = models.Author(
            name="test", email="test@example.com", summary="test author summary"
        )
        author.save()

        # print(list(models.Author.objects.all().values()))        
        
        response = self.client.post(reverse("blogs"), data=dumps({
            "title": "test blog", "content": "tests blog content", "author": "test"
        }), content_type="json")
        self.assertEqual(response.status_code, 201)

    def test_post_add_new_blog_when_author_not_given(self):
        # print("--- test_post_add_new_blog_when_author_not_given ---")

        response = self.client.post(reverse("blogs"), data=dumps({
            "title": "test blog", "content": "test blog content"
        }), content_type="json")
        self.assertEqual(response.status_code, 400)

    def test_post_add_new_blog_when_content_not_given(self):
        # print("--- test_post_add_new_blog_when_content_not_given ---")

        author = models.Author(
            name="test", email="test@example.com", summary="test author summary"
        )
        author.save()

        # print(list(models.Author.objects.all().values())) 

        response = self.client.post(reverse("blogs"), data=dumps({
            "title": "test blog", "author": author.name
        }), content_type="json")
        self.assertEqual(response.status_code, 400)

    def test_post_update_blog_when_blog_not_exists(self):

        # print("--- test_post_update_blog_when_blog_not_exists ---")

        # print(list(models.Author.objects.all().values())) 
        # print(list(models.Blog.objects.all().values())) 

        response = self.client.post(reverse("blogs"), data=dumps({
            "id": 1, "title": "test blog", "content": "test blog content"
        }), content_type="json")
        self.assertEqual(response.status_code, 404)

    def test_post_update_blog_when_blog_exists(self):
        # print("--- test_post_update_blog_when_blog_exists ---")

        author = models.Author(
            name="test", email="test@example.com", summary="test author summary"
        )
        author.save()

        # print(list(models.Author.objects.all().values())) 

        blog = models.Blog(
            title="test blog", content="test blog content",
            author=author, pub_date=timezone.now()
        )
        blog.save()

        # print(list(models.Blog.objects.all().values()))

        response = self.client.post(reverse("blogs"), data=dumps({
            "id": blog.id, "title": "test blog updated", "content": "test blog content updated"
        }), content_type="json")
        self.assertEqual(response.status_code, 200)

    def test_post_update_blog_when_new_author_exists(self):
        # print("--- test_post_update_blog_when_new_author_exists ---")

        author = models.Author(
            name="test", email="test@example.com", summary="test author summary"
        )
        author.save()

        # print(list(models.Author.objects.all().values())) 

        blog = models.Blog(
            title="test blog", content="test blog content",
            author=author, pub_date=timezone.now()
        )
        blog.save()

        # print(list(models.Blog.objects.all().values()))

        new_author = models.Author(
            name="other", email="other@example.com", summary="other author summary"
        )
        new_author.save()

        # print(list(models.Author.objects.all().values()))

        response = self.client.post(reverse("blogs"), data=dumps({
            "id": blog.id, "title": "test blog updated", "content": "test blog content updated",
            "author": new_author.name
        }), content_type="json")
        self.assertEqual(response.status_code, 200)

    def test_post_update_blog_when_new_author_not_exists(self):
        # print("--- test_post_update_blog_when_new_author_not_exists ---")

        author = models.Author(
            name="test", email="test@example.com", summary="test author summary"
        )
        author.save()

        # print(list(models.Author.objects.all().values())) 

        blog = models.Blog(
            title="test blog", content="test blog content",
            author=author, pub_date=timezone.now()
        )
        blog.save()

        # print(list(models.Blog.objects.all().values()))

        response = self.client.post(reverse("blogs"), data=dumps({
            "id": blog.id, "title": "test blog updated", "content": "test blog content updated",
            "author": "other"
        }), content_type="json")
        self.assertEqual(response.status_code, 404)

    def test_delete_when_blog_id_is_none_or_blog_not_exists(self):
        # print("--- test_delete_when_blog_id_is_none_or_blog_not_exists ---")
        
        # print(list(models.Blog.objects.all().values()))

        response = self.client.delete(reverse("blogs_with_id", args=[1]))
        self.assertEqual(response.status_code, 400)

    def test_delete_when_blog_with_given_id_exists(self):
        # print("--- test_delete_when_blog_with_given_id_exists ---")
        
        author = models.Author(
            name="test", email="test@example.com", summary="test author summary"
        )
        author.save()

        # print(list(models.Author.objects.all().values())) 

        blog = models.Blog(
            title="test blog", content="test blog content",
            author=author, pub_date=timezone.now()
        )
        blog.save()

        # print(list(models.Blog.objects.all().values()))

        response = self.client.delete(reverse("blogs_with_id", args=[blog.id]))
        self.assertEqual(response.status_code, 200)

        # print(list(models.Blog.objects.all().values()))

    def test_blog_view_method_not_implemented(self):
        # print("--- test_blog_view_method_not_implemented ---")

        response = self.client.put(reverse("blogs"))
        self.assertEqual(response.status_code, 501)

class AuthorViewTests(TestCase):

    client = Client()

    def test_get_request_when_author_id_is_none(self):
        # print("--- test_get_request_when_author_id_is_none ---")
        
        response = self.client.get(reverse("authors"))
        self.assertEqual(response.status_code, 400)

    def test_get_request_when_author_id_is_not_none_and_author_exists(self):
        # print("--- test_get_request_when_author_id_is_not_none_and_author_exists ---")

        author = models.Author(
            name="test", email="test@example.com", summary="test author summary"
        )
        author.save()

        # print(list(models.Author.objects.all().values()))  
        
        response = self.client.get(reverse("authors_with_id", args=[author.id]))
        self.assertEqual(response.status_code, 200)

    def test_get_request_when_author_id_is_not_none_and_author_not_exists(self):
        # print("--- test_get_request_when_author_id_is_not_none_and_author_not_exists ---")

        response = self.client.get(reverse("authors_with_id", args=[1]))
        self.assertEqual(response.status_code, 404)

    def test_post_request_when_author_id_is_not_none(self):
        # print("--- test_post_request_when_author_id_is_not_none ---")
        
        response = self.client.post(reverse("authors_with_id", args=[1]))
        self.assertEqual(response.status_code, 400)

    def test_post_request_when_author_id_is_none_and_request_body_invalid(self):
        # print("--- test_post_request_when_author_id_is_none_and_request_body_invalid ---")

        response = self.client.post(reverse("authors"))
        self.assertEqual(response.status_code, 400)

    def test_post_add_new_author_when_email_or_summary_not_provided(self):
        # print("--- test_post_add_new_author_when_email_or_summary_not_provided ---")

        response = self.client.post(reverse("authors"), data=dumps({
            "name": "test",
        }), content_type="json")
        self.assertEqual(response.status_code, 400)

    def test_post_add_new_author(self):
        # print("--- test_post_add_new_author ---")

        response = self.client.post(reverse("authors"), data=dumps({
            "name": "test", "email": "email@example.com", "summary": "test author summary"
        }), content_type="json")
        self.assertEqual(response.status_code, 201)
    
    def test_post_update_author_when_author_not_exists(self):
        # print("--- test_post_update_author_when_author_not_exists ---")
        
        # print(list(models.Author.objects.all().values()))

        response = self.client.post(reverse("authors"), data=dumps({
            "id": 1, "name": "test author updated", "email": "testupdated@example.com",
        }), content_type="json")

        self.assertEqual(response.status_code, 404)

    def test_post_update_author_when_author_exists(self):
        # print("--- test_post_update_author_when_author_exists ---")

        author = models.Author(
            name="test", email="test@example.com", summary="test author summary"
        )
        author.save()

        response = self.client.post(reverse("authors"), data=dumps({
            "id": author.id, "name": "test author updated", "email": "testupdated@example.com",
            "summary": "test author summary updated"
        }), content_type="json")
        self.assertEqual(response.status_code, 200)

    def test_delete_when_author_id_is_none_or_author_not_exists(self):
        # print("--- test_delete_when_author_id_is_none_or_author_not_exists ---")
        
        response = self.client.delete(reverse("authors_with_id", args=[1]))
        self.assertEqual(response.status_code, 400)

    def test_delete_when_author_with_given_id_exists(self):
        # print("--- test_delete_when_author_with_given_id_exists ---")

        author = models.Author(
            name="test", email="test@example.com", summary="test author summary"
        )
        author.save()

        # print(list(models.Author.objects.all().values()))

        response = self.client.delete(reverse("authors_with_id", args=[author.id]))
        self.assertEqual(response.status_code, 200)

        # print(list(models.Author.objects.all().values()))

    def test_author_view_method_not_implemented(self):
        # print("--- test_author_view_method_not_implemented ---")

        response = self.client.put(reverse("authors"))
        self.assertEqual(response.status_code, 501)

class ModelReprTests(TestCase):

    def test_blog_repr(self):
        # print("--- test_blog_repr ---")
        
        author = models.Author(
            name="test", email="test@example.com", summary="test author summary"
        )
        author.save()

        # print(list(models.Author.objects.all().values())) 

        time = timezone.now()
        blog = models.Blog(
            title="test blog", content="test blog content",
            author=author, pub_date=time
        )
        blog.save()

        # print(list(models.Blog.objects.all().values()))

        self.assertEqual(
            str(blog), 
            f"Blog(title=test blog, author=Author(name=test, email=test@example.com), pub_date={str(time)})"
        )

    def test_author_repr(self):
        # print("--- test_author_repr ---")

        author = models.Author(
            name="test", email="test@example.com", summary="test author summary"
        )
        author.save()

        # print(list(models.Author.objects.all().values())) 

        self.assertEqual(str(author), "Author(name=test, email=test@example.com)")
