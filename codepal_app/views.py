from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .models import Profile, Project, Review, Like, Follow
from .serializers import ProfileSerializer, ProjectSerializer, LikeSerializer, ReviewSerializer, FollowSerializer, UserSerializer

class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = []

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = User.objects.get(username=response.data['username'])

        profile_data = {
            'profile_picture': request.data.get('profile_picture', ''),
            'description': request.data.get('description', ''),
            'location': request.data.get('location', ''),
            'portfolio_link': request.data.get('portfolio_link', ''),
            'role': request.data.get('role', ''),
            'is_developer': request.data.get('is_developer', False)
        }
        profile_serializer = ProfileSerializer(data=profile_data)
        if profile_serializer.is_valid():
            profile_serializer.save(user=user)
        else:
            return Response(profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': response.data,
            'profile': profile_serializer.data
        }, status=status.HTTP_201_CREATED)


class EditUserView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()


class DeleteUserView(generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()

# User Login
class LoginView(APIView):
  permission_classes = [permissions.AllowAny]

  def post(self, request):
    username = request.data.get('username')
    password = request.data.get('password')
    print(username, password)
    user = authenticate(username=username, password=password)
    if user:
      profile = Profile.objects.get(user=user)
      refresh = RefreshToken.for_user(user)
      return Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'user': UserSerializer(user).data,
        'profile': ProfileSerializer(profile).data
      })
    return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

# User Verification
class VerifyUserView(APIView):
  permission_classes = [permissions.IsAuthenticated]

  def get(self, request):
    user = User.objects.get(username=request.user)
    profile = Profile.objects.get(user=user)
    refresh = RefreshToken.for_user(request.user)
    return Response({
      'refresh': str(refresh),
      'access': str(refresh.access_token),
      'user': UserSerializer(user).data,
      'profile': ProfileSerializer(profile).data
    })

class Home(APIView):
  def get(self, request):
    content = {'message': 'Welcome to the codePal API'}
    return Response(content)

class ProfileList(generics.ListAPIView):
  queryset = Profile.objects.all()
  serializer_class = ProfileSerializer

class DeveloperList(generics.ListAPIView):
  queryset = Profile.objects.filter(is_developer= True)
  serializer_class = ProfileSerializer

class FullStackList(generics.ListAPIView):
  queryset = Profile.objects.filter(role="FS")
  serializer_class = ProfileSerializer

class FrontendList(generics.ListAPIView):
  queryset = Profile.objects.filter(role="FE")
  serializer_class = ProfileSerializer

class BackendList(generics.ListAPIView):
  queryset = Profile.objects.filter(role="BE")
  serializer_class = ProfileSerializer

class UserExperienceList(generics.ListAPIView):
  queryset = Profile.objects.filter(role="UX")
  serializer_class = ProfileSerializer

class ProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = 'id'

    def perform_update(self, serializer):
        profile = self.get_object()
        if profile.user != self.request.user:
            raise PermissionDenied({"message": "You do not have permission to edit this profile."})
        serializer.save()

class ProjectList(generics.ListCreateAPIView):
    serializer_class = ProjectSerializer

    def get_queryset(self):
      profile_id = self.kwargs.get('id')
      return Project.objects.filter(profile_id=profile_id)

    
    def post(self, request, id):  # Add 'id' parameter to match the URL pattern
        profile_id = id  # Get the profile ID from the URL kwargs
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(profile_id=profile_id)  # Assuming 'user_id' is the field representing the profile in Project model
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
class ProjectDelete(generics.RetrieveUpdateDestroyAPIView):
  queryset = Project.objects.all()
  serializer_class = ProjectSerializer
  lookup_field = 'profile_id'

  def perform_destroy(self, instance):
    instance.delete()


class LikeDetail(generics.RetrieveUpdateDestroyAPIView):
    def get(self, request, id):
        like = get_object_or_404(Like, id=id)
        serializer = LikeSerializer(like)
        return Response(serializer.data)

    def post(self, request):
        serializer = LikeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, id):
        like = get_object_or_404(Like, id=id)
        like.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class ReviewList(generics.ListAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
      profile_id = self.kwargs['id']
      return Review.objects.filter(reviewed_user_id=profile_id)

class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def perform_update(self, serializer):
        review = self.get_object()
        if review.reviewer.user != self.request.user:
            raise PermissionDenied({"message": "You do not have permission to edit this review."})
        serializer.save()

    def perform_destroy(self, instance):
        if instance.reviewer.user != self.request.user:
            raise PermissionDenied({"message": "You do not have permission to delete this review."})
        instance.delete()
    
class FollowDetail(APIView):
    def get(self, request, follower_id, following_id):
        follow = get_object_or_404(Follow, follower_id=follower_id, following_id=following_id)
        serializer = FollowSerializer(follow)
        return Response(serializer.data)

    def delete(self, request, follower_id, following_id):
        follow = get_object_or_404(Follow, follower_id=follower_id, following_id=following_id)
        follow.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# class UserJoinProfile(APIView):
#    def get(self):
#       user = User.objects.filter(id = self)
#       profile = Profile.objects.filter(user = self )
#       serializer_class = ProfileSerializer
#       serializer_class = UserSerializer
#       joinedUserInfo = {user, profile}
#       return joinedUserInfo

class UserJoinProfile(APIView):
    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        profile = Profile.objects.get(user=user)
        user_serializer = UserSerializer(user)
        profile_serializer = ProfileSerializer(profile)
        joined_user_info = {
            'user': user_serializer.data,
            'profile': profile_serializer.data
        }
        return Response(joined_user_info)

class FollowsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        profile = get_object_or_404(Profile, user=user)

        # Get profiles who are followers of the authenticated user's profile
        followers = Profile.objects.filter(Followed__following=profile)

        # Get profiles that are followed by the authenticated user's profile
        following = Profile.objects.filter(Following__follower=profile)

        # Serialize the data
        followers_serializer = ProfileSerializer(followers, many=True)
        following_serializer = ProfileSerializer(following, many=True)

        # Return the data in the desired format
        return Response({
            'followers': followers_serializer.data,
            'following': following_serializer.data
        })