from rest_framework import serializers
from .models import Profile, Project, Review, Like, Follow
from django.contrib.auth.models import User

from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username', 'password', 'email')
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},  # Specify password field as write-only
        }     
    
    def create(self, validated_data):
        user = User.objects.create_user(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password']
        )
        print(user)
        return user
    
    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.username = validated_data.get('username', instance.username)
        password = validated_data.get('password')

        if password:
            instance.set_password(password)

        instance.save()
        return instance

    def delete(self, instance):
        instance.delete()

class ProfileSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super(ProfileSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request', None)
        if request and request.method in ['PUT', 'PATCH']:
            self.fields['user'] = UserSerializer(context=self.context)
        else:
            self.fields['user'] = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = '__all__'
        extra_kwargs = {
            'image_url': {'required': False, 'source': 'profile_picture'}
        }

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        if user_data:
            user_serializer = UserSerializer(instance.user, data=user_data, context=self.context, partial=True)
            if user_serializer.is_valid(raise_exception=True):
                user_serializer.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

# class ProfileSerializer(serializers.ModelSerializer):
#     user = serializers.SerializerMethodField()
#     image_url = serializers.ImageField(required=False)

#     class Meta:
#         model = Profile
#         fields = '__all__'

#     def get_user(self, obj):
#         # Always serialize the user information
#         serializer = UserSerializer(obj.user)
#         return serializer.data

#     def to_representation(self, instance):
#         # This method controls how instances are converted to complex datatypes,
#         # modifying it to handle dynamic read-only fields based on context.
#         ret = super().to_representation(instance)
#         request = self.context.get('request')
#         if request and request.method in ['POST', 'PUT', 'PATCH']:
#             # Make user field writable if it's a POST/PUT/PATCH request
#             ret['user'] = UserSerializer(instance.user, context=self.context).data
#         return ret

#     def update(self, instance, validated_data):
#         user_data = validated_data.pop('user', None)
#         if user_data:
#             user_serializer = UserSerializer(instance.user, data=user_data, context={'request': self.context.get('request')})
#             if user_serializer.is_valid(raise_exception=True):
#                 user_serializer.save()

#         for attr, value in validated_data.items():
#             setattr(instance, attr, value)
#         instance.save()
#         return instance

# class ProfileSerializer(serializers.ModelSerializer):
#     user = UserSerializer(read_only=True)
#     image_url = serializers.ImageField(required=False)
#     class Meta:
#         model = Profile
#         fields = '__all__'

#     def update(self, instance, validated_data):
#         print("I am the validated data: ",validated_data)
#         user_data = validated_data.pop('user')
#         user_serializer = UserSerializer(instance.user, data=user_data)
#         if user_serializer.is_valid(raise_exception=True):
#             user_serializer.save()

#         for attr, value in validated_data.items():
#             setattr(instance, attr, value)
#         instance.save()
#         return instance

class ProjectSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Project
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    reviewer = ProfileSerializer(read_only=True)
    reviewed_user = ProfileSerializer(read_only=True)

    class Meta:
        model = Review
        fields = '__all__'

    def create(self, validated_data):
        return Review.objects.create(**validated_data)

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
