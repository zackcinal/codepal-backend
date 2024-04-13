from rest_framework import serializers
from .models import Profile, Project, Review, Like, Follow
from django.contrib.auth.models import User

from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username', 'password')
        extra_kwargs = {
            'password': {'write_only': True},  # Specify password field as write-only
        }     
    
    def create(self, validated_data):
        user = User.objects.create_user(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            username=validated_data['username'],
            password=validated_data['password']
        )
        print(user)
        return user
    
    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.username = validated_data.get('username', instance.username)
        password = validated_data.get('password')
        if password:
            instance.set_password(password)
        instance.save()
        return instance

    def delete(self, instance):
        instance.delete()


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    image_url = serializers.ImageField(required=False)
    class Meta:
        model = Profile
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

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
