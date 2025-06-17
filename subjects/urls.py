from django.urls import path
from . import views

urlpatterns = [
    path('', views.SubjectListView.as_view(), name='subject_list'),
    path('create/', views.SubjectCreateView.as_view(), name='subject_create'),
    path('<int:pk>/', views.SubjectDetailView.as_view(), name='subject_detail'),
    path('<int:pk>/update/', views.SubjectUpdateView.as_view(), name='subject_update'),
    path('<int:pk>/delete/', views.SubjectDeleteView.as_view(), name='subject_delete'),

    # Topic URLs
    path('<int:subject_pk>/topics/create/', views.TopicCreateView.as_view(), name='topic_create'),
    path('topics/<int:pk>/', views.TopicDetailView.as_view(), name='topic_detail'),
    path('topics/<int:pk>/update/', views.TopicUpdateView.as_view(), name='topic_update'),
    path('topics/<int:pk>/delete/', views.TopicDeleteView.as_view(), name='topic_delete'),
    path('topics/<int:topic_pk>/documents/upload/', views.DocumentUploadForTopicView.as_view(), name='topic_document_upload'),

    # Document URLs
    path('documents/', views.DocumentListView.as_view(), name='document_list'),
    path('<int:subject_pk>/documents/upload/', views.DocumentUploadView.as_view(), name='document_upload'),
    path('documents/upload/', views.DocumentUploadFromListView.as_view(), name='document_upload_from_list'),
    path('documents/<int:pk>/delete/', views.DocumentDeleteView.as_view(), name='document_delete'),
]
