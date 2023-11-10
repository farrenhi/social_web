from django.shortcuts import render

from .models import Profile

# Create your views here.


def my_profile_view(request):
    profile = Profile.objects.get(user=request.user)
    # get profile based on logined user
    
    
    context = {
        'profile': profile,
    }
    
    # include the name of application into the html path (in case of confustion)
    return render(request, 'profiles/myprofile.html', context)