import json

from django.db import connection
from django.http import HttpRequest
from django.http import JsonResponse
from django.utils import timezone

from . import models

def blogs(request: HttpRequest, blog_id=None):
    
    if request.method == "GET":
        if blog_id is not None:
            query_response = models.Blog.objects.raw(
                """
                SELECT * FROM crudapp_blog 
                WHERE id = %s
                """
            , [blog_id])
            response_body = []
            for blog in query_response:
                response_body.append({
                    "id": blog.id,
                    "title": blog.title,
                    "content": blog.content,
                    "publication_date": blog.pub_date,
                    "author_id": blog.author_id,
                })
            print(query_response, response_body)
            
            if not response_body:
                return JsonResponse({
                    "status": 404,
                    "message": f"Not found. No data found for blog_id={blog_id}"
                }, status=404)
            else:
                return JsonResponse({
                    "status": 200, "message": "Ok", "data": response_body
                }, safe=False, status=200)
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
            })
        else:
            try:
                request_body = json.loads(request.body)

                if "id" in request_body:
                    try:

                        query_response = models.Blog.objects.raw(
                            """
                            SELECT * FROM crudapp_blog 
                            WHERE id = %s
                            """
                        , [int(request_body["id"])])

                        before_update = []
                        for blog in query_response:
                            before_update.append({
                                "id": blog.id,
                                "title": blog.title,
                                "content": blog.content,
                                "author_id": blog.author_id,
                                "pub_date": blog.pub_date
                            })

                        if "title" in request_body:
                            with connection.cursor() as cursor:
                                cursor.execute(
                                    """
                                    UPDATE crudapp_blog
                                    SET title = %s
                                    WHERE id = %s
                                    """
                                , [request_body["title"], request_body["id"]])

                        if "content" in request_body:
                            with connection.cursor() as cursor:
                                cursor.execute(
                                    """
                                    UPDATE crudapp_blog
                                    SET content = %s
                                    WHERE id = %s
                                    """
                                , [request_body["content"], request_body["id"]])

                        if "author" in request_body:
                            try:
                            
                                query_response = models.Author.objects.raw(
                                    """
                                    SELECT crudapp_blog.id, crudapp_blog.author_id
                                    FROM crudapp_blog
                                    WHERE crudapp_blog.id = %s
                                    """
                                , [request_body["id"]])
                                old_author_id = query_response[0].author_id if query_response else None

                                query_response = models.Author.objects.raw(
                                    """
                                    SELECT crudapp_author.id
                                    FROM crudapp_author
                                    WHERE crudapp_author.name LIKE %s
                                    """
                                , [request_body["author"]])

                                new_author_id = query_response[0].id if query_response else None

                                print(new_author_id, old_author_id)

                                if all((old_author_id, new_author_id)) and old_author_id != new_author_id:
                                    with connection.cursor() as cursor:
                                        cursor.execute(
                                            """
                                            UPDATE crudapp_blog
                                            SET author_id = %s
                                            WHERE id = %s
                                            """
                                        , [new_author_id, request_body["id"]])

                            except Exception as e:
                                return JsonResponse({
                                    "status": 404,
                                    "message": f"Not found. Author with name='{request_body['author']}' not found. Please provide valid Author or create new Author."
                                }, status=404)        

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
                      
                        query_response = models.Author.objects.raw(
                            """
                            SELECT crudapp_author.id, crudapp_author.name 
                            FROM crudapp_author
                            WHERE crudapp_author.name LIKE %s
                            """
                        , [request_body["author"]])

                        blog_author_id = query_response[0].id if query_response else None

                        if blog_author_id:
                            try:
                      
                                with connection.cursor() as cursor:
                                    cursor.execute(
                                        """
                                        INSERT INTO crudapp_blog (title, content, author_id, pub_date)
                                        VALUES (%s, %s, %s, DATE(%s))
                                        RETURNING id
                                        """
                                    , [request_body["title"], request_body["content"], blog_author_id, timezone.now().isoformat()])
                                    query_response = cursor.fetchone()
                                    new_blog_id = query_response[0]

                                print(new_blog_id)

                                return JsonResponse({
                                    "status": 201,
                                    "message": "Created. New blog details added successfully.",
                                    "data": list(models.Blog.objects.filter(pk=new_blog_id).values())
                                }, status=201)

                            except Exception as e:
                                return JsonResponse({
                                    "status": 400,
                                    "message": "Bad request. Please provide all required values: title, content and author.",
                                }, status=400)
                                
                        else:
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

            query_response = models.Blog.objects.raw(
                """
                SELECT * FROM crudapp_blog
                WHERE id = %s
                """
            , [blog_id])
 
            before_delete = []
            for blog in query_response:
                before_delete.append({
                    "id": blog.id,
                    "title": blog.title,
                    "content": blog.content,
                    "publication_date": blog.pub_date,
                    "author_id": blog.author_id
                })
            
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    DELETE FROM crudapp_blog
                    WHERE id = %s
                    """
                , [blog_id])
            
            return JsonResponse({
                "status": 200,
                "message": "Ok. Data deleted successfully",
                "deleted_data": before_delete
            }, safe=False, status=200)
            
        except Exception as e:
            print(e)
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
                query_response = models.Author.objects.raw(
                    """
                    SELECT * FROM crudapp_author
                    WHERE id = %s
                    """
                , [author_id])
                response_body = []
                for author in query_response:
                    response_body.append({
                        "id": author.id,
                        "name": author.name,
                        "email": author.email,
                        "summary": author.summary
                    })
                return JsonResponse({
                    "status": 200, "message": "Ok", "data": response_body
                }, safe=False, status=200)
        else:
            return JsonResponse({
                "status": 400,
                "message": "Bad request. Please provide valid `author_id` to get Author details."
            }, status=400)

    elif request.method == "POST":

        try:
            request_body = json.loads(request.body)

            if "id" in request_body:
                query_response = models.Author.objects.raw(
                    """
                    SELECT * FROM crudapp_author
                    WHERE id = %s
                    """
                , [int(request_body["id"])])
                before_update = []
                for author in query_response:
                    before_update.append({
                        "id": author.id,
                        "name": author.name,
                        "email": author.email,
                        "summary": author.summary
                    })

                try:

                    if "name" in request_body:
                        with connection.cursor() as cursor:
                            cursor.execute(
                                """
                                UPDATE crudapp_author
                                SET name = %s
                                WHERE id = %s
                                """
                            , [request_body["name"], int(request_body["id"])])
    
                    if "email" in request_body:
                        with connection.cursor() as cursor:
                            cursor.execute(
                                """
                                UPDATE crudapp_author
                                SET email = %s
                                WHERE id = %s
                                """
                            , [request_body["email"], int(request_body["id"])])

                    if "summary" in request_body:
                        with connection.cursor() as cursor:
                            cursor.execute(
                                """
                                UPDATE crudapp_author
                                SET summary = %s
                                WHERE id = %s
                                """
                            , [request_body["summary"], int(request_body["id"])])


                    query_response = models.Author.objects.raw(
                        """
                        SELECT * FROM crudapp_author
                        WHERE id = %s
                        """
                    , [int(request_body["id"])])
                    after_update = []
                    for author in query_response:
                        after_update.append({
                            "id": author.id,
                            "name": author.name,
                            "email": author.email,
                            "summary": author.summary
                        })

                    return JsonResponse({
                        "status": 200,
                        "message": "Ok. Author details updated successfully.",
                        "before_update": before_update,
                        "after_update": after_update 
                    }, safe=False, status=200)

                except Exception as e:
                    print(e)
                    return JsonResponse({
                        "status": 404,
                        "message": f"Not found. Author with author_id='{request_body['id']}' not found. Please provide valid author_id."
                    }, status=404)
                            
            else:
            
                try:

                    with connection.cursor() as cursor:
                        cursor.execute(
                            """
                            INSERT INTO crudapp_author (name, email, summary)
                            VALUES (%s, %s, %s)
                            RETURNING id
                            """
                        , [request_body["name"], request_body["email"], request_body["summary"]])
                        # RETURNING id -- returns id of newly inserted row
                        query_response = cursor.fetchone()
                        new_author_id = query_response[0]

                    query_response = models.Author.objects.raw(
                        """
                        SELECT * FROM crudapp_author
                        WHERE id = %s
                        """
                    , [new_author_id])
                    response_body = []
                    for author in query_response:
                        response_body.append({
                            "id": author.id,
                            "name": author.name,
                            "email": author.email,
                            "summary": author.summary
                        })
                    return JsonResponse({
                        "status": 201,
                        "message": "Created. New author details added successfully.",
                        "data": response_body
                    }, safe=False, status=201)

                except Exception as e:
                    print(e)
                    return JsonResponse({
                        "status": 400,
                        "message": "Bad request. Please provide all required values: name, email and summary.",
                    }, status=400)
        
        except Exception as e:
            print(e)
            return JsonResponse({
                "status": 400,
                "message": "Bad request. Please either provide new author details to Add or existing author details to Update."
            }, status=400)

    elif request.method == "DELETE":
        try:

            query_response = models.Author.objects.raw(
                """
                SELECT * FROM crudapp_author
                WHERE id = %s
                """
            , [author_id])
 
            before_delete = []
            for author in query_response:
                before_delete.append({
                    "id": author.id,
                    "name": author.name,
                    "email": author.email,
                    "summary": author.summary
                })
            
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    DELETE FROM crudapp_author
                    WHERE id = %s
                    """
                , [author_id])
            
            return JsonResponse({
                "status": 200,
                "message": "Ok. Data deleted successfully",
                "deleted_data": before_delete
            }, safe=False, status=200)

        except Exception as e:
            print(e)
            return JsonResponse({
                "status": 400,
                "message": f"Bad request. Please provide valid `author_id` to delete Author."
            }, status=400)

    else:
        return JsonResponse({
            "status": 501,
            "message": f"Not Implemented. Method '{request.method}' is not implemented on this endpoint."
        })
