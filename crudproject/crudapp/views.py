import json

from django.db import connection
from django.http import HttpRequest
from django.http import JsonResponse
from django.utils import timezone

from . import models

def blogs(request: HttpRequest, blog_id=None):
    
    if request.method == "GET":
        if blog_id is not None:
            blog = models.Blog.objects.filter(pk=blog_id)            
            if not blog:
                return JsonResponse({
                    "status": 404,
                    "message": f"Not found. No data found for blog_id={blog_id}"
                }, status=404)
            else:
                return JsonResponse({
                    "status": 200, "message": "Ok", "data": list(blog.values())
                }, status=200)                
        else:
            return JsonResponse({
                "status": 400,
                "message": "Bad request. Please provide valid `blog_id` to get Blog details."
            }, status=400)

    elif request.method == "POST":
        if blog_id is not None:
            return JsonResponse({
                "status": 400,
                "message": "Bad request. Please don't include blog_id in url, provide it in request body instead."
            }, status=400)
        else:
            try:
                request_body = json.loads(request.body)
                if "id" in request_body:
                    try:

                        before_update = list(models.Blog.objects.filter(pk=int(request_body["id"])).values())

                        blog = models.Blog.objects.get(pk=int(request_body["id"]))

                        if "title" in request_body:
                            blog.title = request_body["title"]

                        if "content" in request_body:
                            blog.content = request_body["content"]

                        if "author" in request_body:
                            try:
                                author = models.Author.objects.get(name__exact=request_body["author"])
                                if author != blog.author:
                                    blog.author = author

                            except Exception as e:
                                return JsonResponse({
                                    "status": 404,
                                    "message": f"Not found. Author with name='{request_body['author']}' not found. Please provide valid Author or create new Author."
                                }, status=404)
                            
                        blog.save()

                        return JsonResponse({
                            "status": 200,
                            "message": "Ok. Blog details updated successfully.",
                            "before_update": before_update,
                            "after_update": list(models.Blog.objects.filter(pk=int(request_body["id"])).values()) 
                        }, status=200)

                    except Exception as e:
                        return JsonResponse({
                            "status": 404,
                            "message": f"Not found. Blog with blog_id='{request_body['id']}' not found. Please provide valid blog_id."
                        }, status=404)
                                
                else:
                    try:
                        try:
                            blog_author = models.Author.objects.get(name__iexact=request_body["author"])
                            try:
                                new_blog = models.Blog(
                                    title=request_body["title"], 
                                    content=request_body["content"], 
                                    author=blog_author,
                                    pub_date=timezone.now()
                                )

                                new_blog.save()

                                return JsonResponse({
                                    "status": 201,
                                    "message": "Created. New blog details added successfully.",
                                    "data": list(models.Blog.objects.filter(pk=new_blog.id).values())
                                }, status=201)
                            except Exception as e:
                                return JsonResponse({
                                    "status": 400,
                                    "message": "Bad request. Please provide all required values: title, content and author.",
                                }, status=400)
                                
                        except Exception as e:
                            return JsonResponse({
                                "status": 404,
                                "message": f"Not found. Blog with Author='{request_body['author']}' not found. Please provide valid Author."
                            }, status=404)    
        
                    except Exception as e:
                        return JsonResponse({
                            "status": 400,
                            "message": f"Bad request. Please provide all required values: title, content and author."
                        }, status=400)
        
            except Exception as e:
                return JsonResponse({
                    "status": 400,
                    "message": "Bad request. Please either provide new blog details to Add or existing blog details to Update."
                }, status=400)

    elif request.method == "DELETE":
        try:
            blog = models.Blog.objects.filter(pk=blog_id)
            before_delete = list(blog.values())
            
            models.Blog.objects.get(pk=blog_id).delete()
            
            return JsonResponse({
                "status": 200,
                "message": "Ok. Data deleted successfully",
                "deleted_data": before_delete
            }, status=200)

            
        except Exception as e:
            return JsonResponse({
                "status": 400,
                "message": f"Bad request. Please provide valid `blog_id` to delete Blog."
            }, status=400)

    else:
        return JsonResponse({
            "status": 501,
            "message": f"Not Implemented. Method '{request.method}' is not implemented on this endpoint."
        }, status=501)    
    
def authors(request: HttpRequest, author_id: int=None):
    
    if request.method == "GET":
        if author_id is not None:
            author = models.Author.objects.filter(pk=author_id)
            if not author:
                return JsonResponse({
                    "status": 404,
                    "message": f"Not found. No data found for author_id={author_id}"
                }, status=404)
            else:
                return JsonResponse({
                    "status": 200, "message": "Ok", "data": list(author.values())
                }, status=200)
        else:
            return JsonResponse({
                "status": 400,
                "message": "Bad request. Please provide valid `author_id` to get Author details."
            }, status=400)

    elif request.method == "POST":

        try:
            request_body = json.loads(request.body)

            if "id" in request_body:
                before_update = list(models.Author.objects.filter(pk=int(request_body["id"])).values())
                
                try:
                    author = models.Author.objects.get(pk=int(request_body["id"]))

                    if "name" in request_body:
                        author.name = request_body["name"]
                
                    if "email" in request_body:
                        author.email = request_body["email"]
                
                    if "summary" in request_body:
                        author.summary = request_body["summary"]
                
                    author.save()

                
                    return JsonResponse({
                        "status": 200,
                        "message": "Ok. Author details updated successfully.",
                        "before_update": before_update,
                        "after_update": list(models.Author.objects.filter(pk=int(request_body["id"])).values()) 
                    }, safe=False, status=200)

                except Exception as e:
                    return JsonResponse({
                        "status": 404,
                        "message": f"Not found. Author with author_id='{request_body['id']}' not found. Please provide valid author_id."
                    }, status=404)
                            
            else:
            
                try:

                    new_author = models.Author(
                        name=request_body["name"], 
                        email=request_body["email"], 
                        summary=request_body["summary"] 
                    )

                    new_author.save()

                    return JsonResponse({
                        "status": 201,
                        "message": "Created. New author details added successfully.",
                        "data": list(models.Author.objects.filter(pk=new_author.id).values())
                    }, status=201)

                except Exception as e:
                    return JsonResponse({
                        "status": 400,
                        "message": "Bad request. Please provide all required values: name, email and summary.",
                    }, status=400)
        
        except Exception as e:
            return JsonResponse({
                "status": 400,
                "message": "Bad request. Please either provide new author details to Add or existing author details to Update."
            }, status=400)

    elif request.method == "DELETE":
        try:
            author = models.Author.objects.filter(pk=author_id)
            before_delete = list(author.values())

            models.Author.objects.get(pk=author_id).delete()

            return JsonResponse({
                "status": 200,
                "message": "Ok. Data deleted successfully",
                "deleted_data": before_delete
            }, status=200)

        except Exception as e:
            return JsonResponse({
                "status": 400,
                "message": f"Bad request. Please provide valid `author_id` to delete Author."
            }, status=400)

    else:
        return JsonResponse({
            "status": 501,
            "message": f"Not Implemented. Method '{request.method}' is not implemented on this endpoint."
        }, status=501)
