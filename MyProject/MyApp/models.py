from django.db import models
from django.utils import timezone
from django.core.validators import validate_slug
from django.contrib.auth.models import User
# Create your models here.
 
# Table for authors: a name (one string), a unique username, a password
# Only if authors registered, can post to the service
# Authors added through admin page. Need at least 2 authors (student, instructor)
class Author(models.Model):
    # Declare an author model
    # Make sure name is one string
    name = models.CharField(max_length=30, validators=[validate_slug])
    # Make sure username is unique
    username = models.CharField(max_length=30, unique=True, primary_key=True)
    password = models.CharField(max_length=30)

    def __str__ (self):
        return 'name: ' + self.name + '\n' + 'username: ' + self.username + '\n' + 'password: ' + self.password

# Table for news stories: 
# A unique key (autogenerated)
# The story headline (limited to 64 characters)
# The story category, which can be one of the following: pol (for politics), art, tech (for technology new), or trivia (for trivial news, e.g. Tom has lost his red socks).
# The story region which can be one of the following: uk, eu (for European news), or w (for world news)
# The story’s author
# The story date
# The story details (limited to 128 characters)
class Story(models.Model):
    # Specify choices for catergory
    CATEGORY_CHOICES = (("pol", "Politics"), ("art", "Art"), ("tech", "Technology"), ("trivia", "Trivia"),)

    # Specify choices for region
    REGION_CHOICES = (("uk", "UK"), ("eu", "Europe"),("w", "World"),)
    
    # Declare a news story model
    headline = models.CharField(max_length=64)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default="*")
    region = models.CharField(max_length=10, choices=REGION_CHOICES, default="*")
    # Make sure the author has valid credentials from an author table and story will be deleted if author no longer exists
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    # Set story date to current date of creation
    date = models.DateField(default=timezone.now)
    details = models.CharField(max_length=128)

    def __str__(self):
        return 'headline: ' + self.headline + '\n' + 'category: ' + self.category + '\n' + 'region: ' + self.region + '\n' + 'details: ' + self.details