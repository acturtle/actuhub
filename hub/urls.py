from django.urls import path
from . import views

urlpatterns = [
    path('', views.ModelListView.as_view(), name='home'),

    # Model
    path('model/', views.ModelListView.as_view(), name='model_list'),
    path('model/add/', views.ModelCreateView.as_view(), name='model_add'),
    path('model/<int:pk>/', views.ModelDetailView.as_view(), name='model_detail'),
    path('model/edit/<int:pk>/', views.ModelUpdateView.as_view(), name='model_edit'),
    path('model/delete/<int:pk>/', views.ModelDeleteView.as_view(), name='model_delete'),

    # Run
    path('run/', views.RunListView.as_view(), name='run_list'),
    path('run/add/', views.RunCreateView.as_view(), name='run_add'),
    path('run/<int:pk>/', views.RunDetailView.as_view(), name='run_detail'),
    path('run/delete/<int:pk>/', views.RunDeleteView.as_view(), name='run_delete'),

    path('api/runs-status/', views.get_runs_status, name='runs_status'),

    # Document
    path('document/', views.DocumentListView.as_view(), name='document_list'),
    path('document/add/', views.DocumentCreateView.as_view(), name='document_add'),
    path('document/<int:pk>/', views.DocumentDetailView.as_view(), name='document_detail'),
    path('document/edit/<int:pk>/', views.DocumentUpdateView.as_view(), name='document_edit'),
    path('document/delete/<int:pk>/', views.DocumentDeleteView.as_view(), name='document_delete'),

    # Machine
    path('machine/', views.MachineListView.as_view(), name='machine_list'),
    path('machine/add/', views.MachineCreateView.as_view(), name='machine_add'),
    path('machine/<int:pk>/', views.MachineDetailView.as_view(), name='machine_detail'),
    path('machine/edit/<int:pk>/', views.MachineUpdateView.as_view(), name='machine_edit'),
    path('machine/delete/<int:pk>/', views.MachineDeleteView.as_view(), name='machine_delete'),
]
