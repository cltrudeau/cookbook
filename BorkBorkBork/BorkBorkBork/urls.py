from django.contrib import admin
from django.urls import path
from django.views.generic.base import RedirectView, TemplateView

from django_distill import distill_path as dpath

from core import views
from core.models import CATEGORIES, Label, Recipe

def get_recipes():
    for recipe in Recipe.objects.all():
        yield {'slug':recipe.slug}


def get_categories():
    for category in CATEGORIES:
        yield {'category_name':category}


def get_labels():
    for label in Label.objects.all():
        yield {'label_name':label.text}


urlpatterns = [
    path('admin/', admin.site.urls),

    # Distill can't handle the 302, uncomment when testing
    #path('favicon.ico', RedirectView.as_view(url='/static/favicon.ico')),

    dpath('', views.home, distill_file='index.html', name='home'),
    dpath('recipe/<str:slug>/', views.recipe, name='recipe',
        distill_func=get_recipes),
    dpath('category/<str:category_name>/', views.category, name='category',
        distill_func=get_categories),
    dpath('label/<str:label_name>/', views.label, name='label',
        distill_func=get_labels),

    dpath('ref_data/', views.ref_data, name='ref_data'),

    dpath('searcher/', TemplateView.as_view(template_name='searcher.html'),
        name='searcher'),
]
