from django.db import models
from django.contrib.auth.models import User

class Milestone(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    milestones = models.ManyToManyField(Milestone, through='ProfileMilestone')

    def __str__(self):
        return self.user.username

class ProfileMilestone(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('under_review', 'Under Internal Review'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
    )
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    milestone = models.ForeignKey(Milestone, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    uploaded_file = models.FileField(upload_to='documents/', blank=True, null=True)

    def __str__(self):
        return f'{self.profile.user.username} - {self.milestone.name}'
