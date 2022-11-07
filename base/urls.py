from django.urls import path 
from django.contrib.auth.decorators import login_required
from . import views


app_name = 'base'

urlpatterns = [
    # HomePage View
    path('', login_required(views.HomePage.as_view()), name='home'),
    # Search
    path('search/', login_required(views.SearchView.as_view()), name='search'),
    # Category
    path('categories/', login_required(views.CategoryList.as_view()), name='category_list'),
    path('categories/add/', login_required(views.CategoryCreate.as_view()), name='category_add'),
    path('categories/search-results/', views.CategorySearchResults.as_view(), name="category_search"),
    path('categories/<slug:slug>/edit/', login_required(views.CategoryEdit.as_view()), name='category_edit'),    
    path('categories/<slug:slug>/delete/', login_required(views.CategoryDelete.as_view()), name='category_delete'),  
    path('categories/<path:hierarchy>/', login_required(views.CategoryDetail.as_view()), name='category'),      
    # Tag
    path('tags/', login_required(views.TagList.as_view()), name='tag_list'),
    path('tags/add/', login_required(views.TagCreate.as_view()), name='tag_add'),
    path('tags/search-results/', views.TagSearchResults.as_view(), name="tag_search"),
    path('tags/<slug:slug>/', login_required(views.TagDetail.as_view()), name='tag'),
    path('tags/<slug:slug>/edit/', login_required(views.TagEdit.as_view()), name='tag_edit'),
    path('tags/<slug:slug>/delete/', login_required(views.TagDelete.as_view()), name='tag_delete'),
] 
