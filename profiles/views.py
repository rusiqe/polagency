from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Profile, ProfileMilestone

@login_required
def profile_view(request):
    profile = get_object_or_404(Profile, user=request.user)
    milestones = ProfileMilestone.objects.filter(profile=profile)
    if request.method == 'POST':
        milestone_id = request.POST.get('milestone_id')
        uploaded_file = request.FILES.get('uploaded_file')
        milestone = get_object_or_404(ProfileMilestone, id=milestone_id, profile=profile)
        milestone.uploaded_file = uploaded_file
        milestone.status = 'under_review'
        milestone.save()
        return redirect('profile')
    return render(request, 'profiles/profile.html', {'profile': profile, 'milestones': milestones})
