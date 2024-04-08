from rest_framework import serializers
from .models import Profile, Project, Review, Like, Follow
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')

    def create(self, validated_data):
      user = User.objects.create_user(
        username=validated_data['username'],
        email=validated_data['email'],
        password=validated_data['password']
      )
      
      return user
      

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Profile
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):
    user = ProfileSerializer()

    class Meta:
        model = Project
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    reviewer = ProfileSerializer()
    reviewed_user = ProfileSerializer()

    class Meta:
        model = Review
        fields = '__all__'

class LikeSerializer(serializers.ModelSerializer):
    liker = ProfileSerializer()
    liked_project = ProjectSerializer()

    class Meta:
        model = Like
        fields = '__all__'

class FollowSerializer(serializers.ModelSerializer):
    follower = ProfileSerializer()
    following = ProfileSerializer()

    class Meta:
        model = Follow
        fields = '__all__'
