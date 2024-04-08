from .views import Home, ProfileList, DeveloperList, ProfileDetail, FullStackList, BackendList, FrontendList, CreateUserView,UserExperienceList, ProjectList, OneReview, LoginView, VerifyUserView
from django.urls import path

urlpatterns = [
  path('', Home.as_view(), name='home'),
  path('users/register/', CreateUserView.as_view(), name='register'),
  path('users/login/', LoginView.as_view(), name='login'),
  path('users/token/refresh/', VerifyUserView.as_view(), name='token_refresh'),
  path('profiles/', ProfileList.as_view(), name="profile-list"),
  path('profiles/<int:id>/', ProfileDetail.as_view(), name="profile-detail"),
  path('profiles/<int:id>/projects/', ProjectList.as_view(), name="project-list"),
  path('profiles/<int:id>/reviews/', OneReview.as_view(), name="one-review-list"),
  path('developers/', DeveloperList.as_view(), name="developer-list"),
  path('developers/fullstack/', FullStackList.as_view(), name="fullstack-list"),
  path('developers/backend/', BackendList.as_view(), name="backend-list"),
  path('developers/frontend/', FrontendList.as_view(), name="frontend-list"),
  path('developers/userexperience/', UserExperienceList.as_view(), name="ux-list"),
]
