from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver


ROLES = (
    ('FS', 'Full Stack Developer'),
    ('FE', 'Front End Developer'),
    ('BE', 'Back End Developer'),
    ('UX', 'User Experience Designer')
)

def upload_to(instance, filename):
    return 'images/{filename}'.format(filename=filename)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to=upload_to, blank=True, null=True)
    description = models.CharField("Description", max_length=255)
    location = models.CharField("Location", max_length=30)
    portfolio_link = models.CharField("Portfolio Link", max_length=1000)
    role = models.CharField("Role",
                              choices=ROLES,
                              max_length=2,
                              default=ROLES[0][0])
    is_developer = models.BooleanField("Are You a Developer?")

    def __str__(self):
        return self.user.username

@receiver(pre_save, sender=User)
def capitalize_user_names(sender, instance, **kwargs):
    instance.first_name = instance.first_name.capitalize()
    instance.last_name = instance.last_name.capitalize()

@receiver(pre_save, sender=Profile)
def capitalize_location(sender, instance, **kwargs):
    instance.location = instance.location.capitalize()

class Project(models.Model):
    title = models.CharField(max_length=50)
    project_image = models.CharField("Project Image", max_length=1000)
    project_description = models.CharField("Project Description", max_length=255)
    project_link = models.CharField("Project Link", max_length=500)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Review(models.Model):
    reviewer = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='reviews_written')
    reviewed_user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='reviews_received')
    review = models.CharField(max_length=200)

    def __str__(self):
        return f"Review by {self.reviewer.user.username} for {self.reviewed_user.user.username}"

class Like(models.Model):
    liker = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='liker')
    liked_project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project_liked')

    def __str__(self):
        return f"Liked by {self.liker.user.username} for {self.liked_project.title}"

class Follow(models.Model):
    follower = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='Followed')
    following = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='Following')
    def __str__(self):
        return f"{self.following.user.username} Followed by {self.follower.user.username}"
