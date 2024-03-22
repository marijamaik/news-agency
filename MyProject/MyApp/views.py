import json
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

# Import created models
from .models import Author, Story
# Create your views here.

# Aim: log in to an author’s account in order to be able to post, or delete news stories.
# The client sends a POST request to /api/login with the following data in an application/x-www-form-
# urlencoded payload with two items:
# 1. Username ("username”, string)
# 2. Password ("password", string)
# If the request is processed successfully, the server responds with 200 OK and a text/plain payload giving some
# welcome message.
# If login fails, the server should respond with the appropriate status code and an explanation (if any) in a
# text/plain payload.
@csrf_exempt
def HandleLogInRequest(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponse("Successfully Logged In as " + user.username, status=200)
        else:
            return HttpResponse("Cannot Log In. Invalid username or password.", status=401)
    else:
        return HttpResponseBadRequest("Bad Request.", status=404)


# Aim: to log out from an author’s account
# The client sends a POST request to /api/logout with no payload.
# If the request is processed successfully, the server responds with 200 OK and a text/plain payload with some
# goodbye message.
# If logout fails, the server should respond with the appropriate status code and an explanation (if any) in a
# text/plain payload.
@csrf_exempt
@login_required
def HandleLogOutRequest(request):
    if request.method == 'POST':
        logout(request)
        return HttpResponse("Log Out Successful.", status=200)
    else:
        return HttpResponseBadRequest("Bad Request. Need to be registered to log out.", status=400)

# Aim: to post a news story
# Pre-condition: the user must be logged in before posting stories
# Service Specifications:
# The client sends a POST request to /api/stories with the following data in a JSON payload. JSON 'key' names
# and value types are given in parenthesis:
# 1. Story headline ("headline", string)
# 2. Story category ("category", string)
# 3. Story region ("region", string)
# 4. Story details ("details", string)
# Upon receipt of this request the server checks that the user is logged in, and if they are the story is added to the
# stories table (with the name of the logged in user) and a time stamp. The server responds with 201 CREATED.
# If the story cannot be added for any reason (e.g. unauthenticated author), the server should respond with 503
# Service Unavailable with text/plain payload giving reason.
@csrf_exempt
@login_required
def HandlePostStoryRequest(request):
    # Post a new story
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            headline = data['headline']
            category = data['category']
            region = data['region']
            details = data['details']
        except KeyError:
            return HttpResponseBadRequest("Missing required fields.", status=400)


        # Check if required fields are provided
        if not (headline and category and region and details):
            return HttpResponseBadRequest("Missing required fields.", status=400)
        

        # Get the logged-in user
        username = request.user
        # Get the associated Author instance
        author = Author.objects.get(username=username)

        # Create and save the story object
        story = Story.objects.create(
            headline=headline,
            category=category,
            region=region,
            author=author,
            date=timezone.now(),
            details=details
        )

        story.save()

        # Return a success response
        return HttpResponse("Story added successfully", status=201)
    else:
        # Return 400 status code for invalid request method
        return JsonResponse({'message': 'Bad request method.'}, status=400)


# Aim: to get news stories
# Service Specifications:
# The client sends a GET request to /api/stories with the following data in an application/x-www-form-
# urlencoded payload with 3 items:
# 1. Story category ("story_cat", string). For any category this should be "*"
# .
# 2. Story region ("story_region", string). For any region this should be "*"
# .
# 3. Story date ("story_date", string). For any date this should be "*"
# .
# When the request is received the server retrieves all stories, having the given category and region published at
# or after the given date. If the request is processed successfully, the server responds with 200 OK and a list of
# stories in a JSON payload (“stories”, array). For each story in the list, the following data must be provided:
# 1. The story’s unique key (“key”, string)
# 2. The story headline ("headline", string)
# 3. The story category ("story_cat" , string)
# 4. The story region ("story_region", string)
# 5. The story author name ("author", string)
# 6. The story date ("story_date", string)
# 7. The story details ("story_details", string)
# If no stories are found, the server should respond with 404 status code with text/plain payload giving more
# information.
@csrf_exempt
def HandleGetStoryRequest(request):
    if request.method == 'GET':
        # Retrieve query parameters from the request
        story_cat = request.GET.get('story_cat', '*')
        story_region = request.GET.get('story_region', '*')
        story_date = request.GET.get('story_date', '*')


        # Filter stories based on provided parameters
        if story_cat == '*' and story_region == '*' and story_date == '*':
            stories = Story.objects.all()
        elif story_cat == '*':
            if story_region == '*':
                stories = Story.objects.filter(
                date__gte=story_date
            )
            elif story_date == '*':
                stories = Story.objects.filter(
                region=story_region
            ) 
            else:
                stories = Story.objects.filter(
                region=story_region,
                date__gte=story_date
            )
        elif story_region == '*':
            if story_date == '*':
                stories = Story.objects.filter(
                category=story_cat
            )
            else:
                stories = Story.objects.filter(
                category=story_cat,
                date__gte=story_date
            )
        elif story_date == '*':
                stories = Story.objects.filter(
                category=story_cat,
                region=story_region
            )
        else:
            stories = Story.objects.filter(
                category=story_cat,
                region=story_region,
                # Using date__gte to find date greater than or equal to the specified date
                date__gte=story_date
            )

        # # Serialize stories into JSON format
        serialized_stories = [{
            'key': story.pk,
            'headline': story.headline,
            'story_cat': story.category,
            'story_region': story.region,
            'author': story.author.username,
            'story_date': story.date.strftime('%d/%m/%Y'),
            'story_details': story.details
        } for story in stories]


    # Check if any stories are found
        if serialized_stories:
            # Return JSON response with stories and status 200
            return JsonResponse({'stories': serialized_stories}, status=200)
        else:
            # Return 404 status code with a message if no stories are found
            return JsonResponse({'message': 'No stories found.'}, status=404)
    else:
        # Return 400 status code for invalid request method
        return JsonResponse({'message': 'Bad request method.'}, status=400)
        
# # Aim: delete a story
# # Pre-condition: user must be logged in
# # Service Specifications:
# # The client sends a DELETE request to /api/stories/key, where /key is the story key.
# # If the request is processed successfully, the server responds with 200 OK.
# # If the server is unable to process the request for any reason, the server should respond with a 503 Service
# # Unavailable with text/plain payload giving reason.
@csrf_exempt
@login_required
def HandleDeleteStoryRequest(request, id):
    try:
        story = Story.objects.get(pk=id)
    except Story.DoesNotExist:
        return HttpResponse("Not Found.", status=404)

    if request.method == 'DELETE':
        if story.author != Author.objects.get(username=request.user):
            return HttpResponse("Unauthorized.", status=403)
        story.delete()
        return HttpResponse("Story Deleted Successfully.", status=200)
    else:
        # If the server is unable to process the request for any reason, the server should respond with a 503 Service Unavailable with text/plain payload giving reason.
        return HttpResponse("Could Not Delete, Server Unable To Process Request.", status=503)