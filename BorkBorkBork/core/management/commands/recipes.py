import re

from pathlib import Path
from types import SimpleNamespace

from django.core.management.base import BaseCommand, CommandError
import toml

from core.models import CategoryType, MEASURES, Label, Recipe

fraction_map = {
    '1/4':'¼',
    '3/4':'¾',
    '1/2':'½',
    '1/3':'⅓',
    '2/3':'⅔',
    '1/8':'⅛',
    '3/8':'⅜',
    '5/8':'⅝',
    '7/8':'⅞',
}

class Command(BaseCommand):
    """Loads recipes TOML files into the database"""

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

        self.help == self.__doc__

    def add_arguments(self, parser):
        parser.add_argument('directory', nargs=1, type=str)

    def _replace_fractions(self, text):
        for key, value in fraction_map.items():
            text = re.sub(key, value, text)

        return text

    def _process_ingredients(self, ingredients):
        for ingredient in ingredients:
            if ingredient[1] not in MEASURES:
                print('      Warning, ingredient measure unknown',
                    ingredient[1])

    def _load_directory(self, path):
        for child in path.iterdir():
            if child.is_dir():
                self._load_directory(child)
            else:
                print(f'   {child.name}')
                try:
                    with child.open() as f:
                        content = self._replace_fractions(f.read())
                        content = toml.loads(content)
                        content = SimpleNamespace(**content)

                        # Manage labels
                        labels = []
                        for label in getattr(content, 'labels', []):
                            label, _ = Label.objects.get_or_create(text=label)
                            if label:
                                labels.append(label)

                        # Create Recipe
                        category = CategoryType[content.category]
                        self._process_ingredients(content.ingredients)

                        description = getattr(content, 'description', '')
                        serves = getattr(content, 'serves', None)
                        cooktime = getattr(content, 'cooktime', None)
                        notes = getattr(content, 'notes', '')

                        recipe = Recipe.objects.create(
                            slug=child.stem,
                            title=content.title,
                            category=category, 
                            serves=serves, 
                            cooktime=cooktime,
                            description=description,
                            ingredients=content.ingredients, 
                            steps=content.steps, 
                            notes=notes
                        )

                        for label in labels:
                            recipe.labels.add(label)
                except Exception as e:
                    print('      Error!', e)

    def handle(self, *args, **options):
        path = Path(options['directory'][0])
        if not path.is_dir():
            CommandError('Directory for recipes must be supplied')

        print('Loading Recipes:')
        self._load_directory(path)
