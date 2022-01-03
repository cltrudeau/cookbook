from itertools import zip_longest
from pathlib import Path

from django.shortcuts import render, get_object_or_404

from core.models import CATEGORIES, CategoryType, Label, Recipe

# ===========================================================================

def global_context_processor(request):
    context = {
        'categories':CATEGORIES,
    }
    return context

# ===========================================================================

def home(request):
    data = {
        'labels':Label.objects.all(),
    }

    return render(request, 'home.html', data)


def recipe(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug)

    data = {
        'active_category':CategoryType(recipe.category).label,
        'recipe':recipe,
        'title':recipe.title,
    }

    return render(request, 'recipe.html', data)


def category(request, category_name):
    category = getattr(CategoryType, category_name)

    recipes = Recipe.objects.filter(category=category)
    recipe_triples = zip_longest(*[iter(recipes)]*3)

    data = {
        'active_category':category.label,
        'recipe_triples':recipe_triples,
        'title':f'Category: {category.label}',
    }

    return render(request, 'category.html', data)


def label(request, label_name):
    label = get_object_or_404(Label, text=label_name)
    recipes = Recipe.objects.filter(labels=label)
    recipe_triples = zip_longest(*[iter(recipes)]*3)

    data = {
        'label':label,
        'recipe_triples':recipe_triples,
        'title':f'Label: {label.text}',
    }

    return render(request, 'label.html', data)


def _child_paths(path, path_list):
    for child in path.iterdir():
        if child.is_dir():
            _child_paths(child)
        else:
            path_list.append(child.name)


def ref_data(request):
    path = Path('../data/recipes/')

    path_list = []
    _child_paths(path, path_list)
    path_list.sort()
    data = {
        'title':'Recipe Source Data',
        'path_list':path_list,
    }
    return render(request, 'ref_data.html', data)
