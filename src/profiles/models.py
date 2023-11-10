from django.db import models
from django.contrib.auth.models import User

from .utils import get_random_code
from django.template.defaultfilters import slugify
# Create your models here.

class Profile(models.Model):
    first_name = models.CharField(max_length=200, blank=True)
    # blank: optional
    last_name = models.CharField(max_length=200, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # one user to one profile. need to use User model
    #  a user is deleted, so a profile is also deleted.
    
    bio = models.TextField(default='fill in my bio...', max_length=300)
    email = models.EmailField(max_length=200, blank=True)
    country = models.CharField(max_length=200, blank=True)
    avatar =models.ImageField(default='avatar.png', upload_to='avatars/')
    # install pillow
    # create media_root
    # find avatar.png
    
    friends = models.ManyToManyField(User, blank=True, related_name='friends')
    
    slug = models.SlugField(unique=True, blank=True)
    # what if many people have same last name and first name?
    
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def get_friends(self):
        return self.friends.all()
    
    def get_friends_no(self):
        return self.friends.all().count()
    
    def __str__(self):
        return f"{self.user.username}-{self.created.strftime('%d-%m-%Y')}"
    
    
    def save(self, *args, **kwargs):
        exist_data = False
        
        if self.first_name and self.last_name:
            to_slug = slugify(str(self.first_name) + " " + str(self.last_name))
            exist_data = Profile.objects.filter(slug=to_slug).exists() # return boolean value
            while exist_data: # if the slug exists!
                to_slug = slugify(to_slug + " " + str(get_random_code()))
                exist_data = Profile.objects.filter(slug=to_slug).exists()
                
        else:
            to_slug = str(self.user)
        
        self.slug = to_slug
        super().save(*args, **kwargs)
        
        # In the save method of the Profile model, super().save(*args, **kwargs) is a call 
        # to the save method of the parent class (models.Model). 
        
        # This is used to perform the actual saving of the instance 
        # in the database.
        

STATUS_CHOICES = (
    ('send', 'send'),
    ('accepted', 'accepted')
)

# (database column name, what we see) 
 
class Relationship(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sender')
    # if the profile is deleted, the relationship will be deleted.
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='receiver')
    status = models.CharField(max_length=8, choices=STATUS_CHOICES)
    # there is where we could change for auto-accept!
    # 8 char for accepted
    
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.sender}-{self.receiver}-{self.status}"