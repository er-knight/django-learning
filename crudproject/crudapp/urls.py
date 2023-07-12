from django.urls import path

from . import views

urlpatterns = [
    path("blogs/", views.blogs, name="blogs"),
    path("blogs/<int:blog_id>/", views.blogs, name="blogs_with_id"),
    path("authors/", views.authors, name="authors"),
    path("authors/<int:author_id>/", views.authors, name="authors_with_id")
]