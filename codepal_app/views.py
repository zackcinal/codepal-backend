from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status, permissions
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

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = User.objects.get(username=response.data['username'])

        # Extract profile-related data from request
        profile_data = {
            'profile_picture': request.data.get('profile_picture', ''),
            'description': request.data.get('description', ''),
            'location': request.data.get('location', ''),
            'portfolio_link': request.data.get('portfolio_link', ''),
            'role': request.data.get('role', ''),
            'is_developer': request.data.get('is_developer', False)
        }

        # Create a Profile object for the user
        profile_serializer = ProfileSerializer(data=profile_data)
        if profile_serializer.is_valid():
            profile_serializer.save(user=user)  # Explicitly set the user here
        else:
            return Response(profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': response.data,
            'profile': profile_serializer.data
        }, status=status.HTTP_201_CREATED)

# User Login
class LoginView(APIView):
  permission_classes = [permissions.AllowAny]

  def post(self, request):
    username = request.data.get('username')
    password = request.data.get('password')
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
    user = User.objects.get(username=request.user)  # Fetch user profile
    profile = Profile.objects.get(user=user)
    refresh = RefreshToken.for_user(request.user)  # Generate new refresh token
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

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied({"message": "You do not have permission to delete this profile."})
        instance.delete()

class ProjectList(generics.ListAPIView):
    serializer_class = ProjectSerializer

    def get_queryset(self):
        profile_id = self.kwargs['id']
        return Project.objects.filter(id=profile_id)
    
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
