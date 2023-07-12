from django.urls import path
from . import views

urlpatterns = [
    path('books/', views.books),
    path('authors/', views.authors),
    path('books/title/<str:title>', views.get_books_by_title),
    path('books/author/<str:author>', views.get_books_by_author),
    path('books/year/<int:publication_year>', views.get_books_by_publication_year),
]