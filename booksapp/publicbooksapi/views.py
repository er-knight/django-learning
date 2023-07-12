import json
import requests

from django.http import HttpResponseNotAllowed, HttpResponseBadRequest, JsonResponse

def books(request):
    request_body_format = {
        "title": "<book-title>",
        "name": "<author-name>",
        "publication_year": "<year>"
    }

    if request.method == "POST":
        try:
            request_body = json.loads(request.body)
            if "title" in request_body and request_body["title"] is not None:
                response = requests.get(f"http://127.0.0.1:8000/booksapi/books/title/{request_body['title']}").json()
                print(response)
                return JsonResponse(response, safe=False)            
            elif "author" in request_body and request_body["author"] is not None:
                response = requests.get(f"http://127.0.0.1:8000/booksapi/books/author/{request_body['author']}").json()
                print(response)
                return JsonResponse(response, safe=False)
            elif "publication_year" in request_body and request_body["publication_year"] is not None:
                response = requests.get(f"http://127.0.0.1:8000/booksapi/books/year/{request_body['publication_year']}").json()
                print(response)
                return JsonResponse(response, safe=False)
            else:
                return HttpResponseBadRequest("Please provide either 'title', 'author' or 'publication_year' in request body.")
        except json.decoder.JSONDecodeError:
            return HttpResponseBadRequest("Please provide a valid and non-empty JSON data in request body.")
    else:
        return HttpResponseNotAllowed(["POST"])
    