from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import Profile, Project, Review, Like, Follow
from .serializers import ProfileSerializer, ProjectSerializer, LikeSerializer, ReviewSerializer, FollowSerializer, UserSerializer

# Create your views here.
class CreateUserView(generics.CreateAPIView):
  queryset = User.objects.all()
  serializer_class = UserSerializer

  def create(self, request, *args, **kwargs):
    response = super().create(request, *args, **kwargs)
    user = User.objects.get(username=response.data['username'])
    refresh = RefreshToken.for_user(user)
    return Response({
      'refresh': str(refresh),
      'access': str(refresh.access_token),
      'user': response.data
    })

# User Login
class LoginView(APIView):
  permission_classes = [permissions.AllowAny]

  def post(self, request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user:
      refresh = RefreshToken.for_user(user)
      return Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'user': UserSerializer(user).data
      })
    return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

# User Verification
class VerifyUserView(APIView):
  permission_classes = [permissions.IsAuthenticated]

  def get(self, request):
    user = User.objects.get(username=request.user)  # Fetch user profile
    refresh = RefreshToken.for_user(request.user)  # Generate new refresh token
    return Response({
      'refresh': str(refresh),
      'access': str(refresh.access_token),
      'user': UserSerializer(user).data
    })


# Define the home view
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

# class CreateProfile(generics.CreateAPIView):


class ProfileDetail(generics.ListAPIView):
    serializer_class = ProfileSerializer

    def get_queryset(self):
        profile_id = self.kwargs['id']
        return Profile.objects.filter(id=profile_id)

    # def perform_update(self, serializer):
    #   cat = self.get_object()
    #   if cat.user != self.request.user:
    #     raise PermissionDenied({"message": "You do not have permission to edit this cat."})
    #   serializer.save()

    # def perform_destroy(self, instance):
    #   if instance.user != self.request.user:
    #     raise PermissionDenied({"message": "You do not have permission to delete this cat."})
    #   instance.delete()

class ProjectList(generics.ListAPIView):
    serializer_class = ProjectSerializer

    def get_queryset(self):
        profile_id = self.kwargs['id']
        return Project.objects.filter(id=profile_id)

class OneReview(generics.ListAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        profile_id = self.kwargs['id']
        return Review.objects.filter(reviewed_user = profile_id)
    
    # def perform_update(self, serializer):
    #   review = self.get_object()
    #   if review.user != self.request.user:
    #     raise PermissionDenied({"message": "You do not have permission to edit this review."})
    #   serializer.save()
    
    
