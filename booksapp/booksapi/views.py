from django.http import HttpResponseNotAllowed, JsonResponse

from . import models

def get_books_by_title(request, title=None):
    if request.method == "GET":
        # return JsonResponse(list(models.Book.objects.filter(title__iexact=title).values()), safe=False)
        response_body = []
        query = f"SELECT * FROM booksapi_book WHERE title = '{title}'"
        for book in models.Book.objects.raw(query):
            print(book)
            response_body.append({
                "id": book.id,
                "title": book.title,
                "author_id": book.author.name,
                "publication_date": book.publication_date,
                "price": book.price
            })
        return JsonResponse(response_body, safe=False)
    else:
        return HttpResponseNotAllowed(["GET"])
    
def get_books_by_author(request, author=None):
    if request.method == "GET":
        # return JsonResponse(list(models.Book.objects.filter(author__name__iexact=author).values()), safe=False)
        response_body = []
        query = f"SELECT * FROM booksapi_book INNER JOIN booksapi_author ON booksapi_book.author_id = booksapi_author.id WHERE booksapi_book.author_id IN (SELECT booksapi_author.id FROM booksapi_author WHERE booksapi_author.name = '{author}') ORDER BY title"
        for book in models.Book.objects.raw(query):
            print(book)
            response_body.append({
                "id": book.id,
                "title": book.title,
                "author_name": book.author.name,
                "publication_date": book.publication_date,
                "price": book.price
            })
        return JsonResponse(response_body, safe=False)
    else:
        return HttpResponseNotAllowed(["GET"])
    
def get_books_by_publication_year(request, publication_year=None):
    if request.method == "GET":
        # return JsonResponse(list(models.Book.objects.filter(publication_date__year=publication_year).values()), safe=False)
        response_body = []
        query = f"SELECT * FROM booksapi_book WHERE DATE_PART('year', booksapi_book.publication_date) = {publication_year} ORDER BY title"
        for book in models.Book.objects.raw(query):
            print(book)
            response_body.append({
                "id": book.id,
                "title": book.title,
                "author_id": book.author.name,
                "publication_date": book.publication_date,
                "price": book.price
            })
        return JsonResponse(response_body, safe=False)
    else:
        return HttpResponseNotAllowed(["GET"]) 

def books(request):
    if request.method == "GET":
        return JsonResponse(list(models.Book.objects.all().values()), safe=False)
    else:
        return HttpResponseNotAllowed(["GET"])
    
def authors(request):
    if request.method == "GET":
        return JsonResponse(list(models.Author.objects.all().values()), safe=False)
    else:
        return HttpResponseNotAllowed(["GET"])
