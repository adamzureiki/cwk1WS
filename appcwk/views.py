from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import json
from .models import News, Author
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.http import require_http_methods



@csrf_exempt
def loginServer(clientRequest):
    # if the client requests to login, we collect credentials 
    if clientRequest.method == "POST":
        if clientRequest.user.is_authenticated:
            # User is already logged in
            return HttpResponse("You are already logged in.", content_type="text/plain", status=200)
        else:
            userName = clientRequest.POST.get("username")
            passcode = clientRequest.POST.get("password")

            # authentication of the credentials 
            loggedIn = authenticate(clientRequest, username=userName, password=passcode)
            if loggedIn is not None:
                login(clientRequest, loggedIn)
                return HttpResponse("You have logged in successfully!", content_type="text/plain", status=200)
            else:
                # using status 401 to show unautherised, this is to not mistakenly flag the isLoggedIn variable in client
                return HttpResponse("Failed login", content_type="text/plain", status=401)
    else:
        return HttpResponse("Failed login.", content_type="text/plain")

@csrf_exempt
def logoutServer(clientRequest):
    if clientRequest.method == "POST":
        if clientRequest.user.is_authenticated:
            logout(clientRequest)
            return HttpResponse("You are now logged out", content_type="text/plain", status=200)
        else:
            return HttpResponse("Cannot logout. You are not logged in", content_type="text/plain")
    else:
        return HttpResponse("Failed logout", content_type="text/plain")
    

# @csrf_exempt
# def postingServer(clientRequest):
#     if clientRequest.method == "POST" and clientRequest.user.is_authenticated:
#         story = json.loads(clientRequest.body)
#         author = Author.objects.get(user=clientRequest.user)
#         try:
#             News.objects.create(
#                 headline=story['headline'],
#                 category=story['category'],
#                 details=story['details'],
#                 region=story['region'],
#                 author=author
#             )
#             return JsonResponse({"message": "Story created"}, status=201)
#         except Exception as e:
#             return HttpResponse(str(e), status=503)
#     else:
#         return JsonResponse({"Error occured": "Either no login or incorrect posting method"})
    
# @csrf_exempt
# def getstoryServer(clientRequest):
#     if clientRequest.method == "GET":

#         # Get parameters or use None as a default to indicate no specific filter
#         cat = clientRequest.GET.get('story_cat', "*")
#         reg = clientRequest.GET.get('story_region', "*")
#         date = clientRequest.GET.get('story_date', "*")
        
#         queryStory = News.objects.all()
#         if cat != '*':
#             queryStory = queryStory.filter(category=cat)
#         if reg != '*':
#             queryStory = queryStory.filter(region=reg)
#         if date != '*':
#             queryStory = queryStory.filter(date__gte=date)


#         # we make a list of stories data
#         metaOfstory =[]
#         for x in queryStory:
#             metaOfstory.append({
#                 "key": x.id,
#                 "headline": x.headline,
#                 "story_cat": x.category,
#                 "story_region": x.region,
#                 "author": x.author.name,
#                 "story_date": x.date.strftime('%Y-%m-%d'),
#                 "story_details": x.details
#             })

#         metaOfstory = []
#         for x in queryStory:
#             metaOfstory.append({
#                 "key": x.id,
#                 "headline": x.headline,
#                 "story_cat": x.category,
#                 "story_region": x.region,
#                 "author": x.author.name,
#                 "story_date": x.date.strftime('%Y-%m-%d'),
#                 "story_details": x.details
#             })
           
#         if metaOfstory:
#             return JsonResponse({"stories": metaOfstory}, status=200)
#         else:
#             return HttpResponse("No stories found.", status=404, content_type="text/plain")
        
@csrf_exempt
def getAndpost (clientRequest):
    if clientRequest.method == "POST" and clientRequest.user.is_authenticated:
        story = json.loads(clientRequest.body)
        author = Author.objects.get(user=clientRequest.user)
        try:
            News.objects.create(
                headline=story['headline'],
                category=story['category'],
                details=story['details'],
                region=story['region'],
                author=author
            )
            return JsonResponse({"message": "Story created"}, status=201)
        except Exception as e:
            return HttpResponse(str(e), status=503)
    elif clientRequest.method == "GET":

        # Get parameters or use None as a default to indicate no specific filter
        cat = clientRequest.GET.get('story_cat', "*")
        reg = clientRequest.GET.get('story_region', "*")
        date = clientRequest.GET.get('story_date', "*")
        
        queryStory = News.objects.all()
        if cat != '*':
            queryStory = queryStory.filter(category=cat)
        if reg != '*':
            queryStory = queryStory.filter(region=reg)
        if date != '*':
            queryStory = queryStory.filter(date__gte=date)


        # we make a list of stories data
        metaOfstory =[]
        for x in queryStory:
            metaOfstory.append({
                "key": x.id,
                "headline": x.headline,
                "story_cat": x.category,
                "story_region": x.region,
                "author": x.author.name,
                "story_date": x.date.strftime('%Y-%m-%d'),
                "story_details": x.details
            })

        metaOfstory = []
        for x in queryStory:
            metaOfstory.append({
                "key": x.id,
                "headline": x.headline,
                "story_cat": x.category,
                "story_region": x.region,
                "author": x.author.name,
                "story_date": x.date.strftime('%Y-%m-%d'),
                "story_details": x.details
            })
           
        if metaOfstory:
            return JsonResponse({"stories": metaOfstory}, status=200)
        else:
            return HttpResponse("No stories found.", status=404, content_type="text/plain")
    else:
        return JsonResponse({"Error occured": "Either no login or incorrect posting method"})