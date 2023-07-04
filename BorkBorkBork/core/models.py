from django.db import models
import mistune
from awl.absmodels import TimeTrackModel

# ===========================================================================

CATEGORIES = ['Appetizers', 'Mains', 'Sauces', 'Desserts', 'Drinks', ]
CategoryType = models.IntegerChoices('CategoryType', ' '.join(CATEGORIES))

MEASURES = ['tsp', 'Tbsp', 'cup', 'cups', 'can', 'ml', 'L', 'g', 'oz', '',
    'lbs', 'pinch', 'clove', 'cloves', 'slice', 'slices', 'dash', 'packet',
    'packets', 'container', 'containers', 'shot', 'shots']

# ===========================================================================

class Label(TimeTrackModel):
    text = models.TextField()

    class Meta:
        ordering = ['text']

    def __str__(self):
        return f'Label(text={self.text})'


class MarkdownContainer:
    def __init__(self, parent):
        self.parent = parent

    def __getattr__(self, attr):
        field = getattr(self.parent, attr)
        return mistune.html(field)


class Recipe(TimeTrackModel):
    slug = models.TextField()
    title = models.TextField()
    category = models.IntegerField(choices=CategoryType.choices)
    description = models.TextField(blank=True)
    serves = models.PositiveSmallIntegerField(blank=True, null=True)
    cooktime = models.PositiveSmallIntegerField(blank=True, null=True)

    ingredients = models.JSONField()
    ingredient_parts = models.JSONField()

    steps = models.TextField()
    notes = models.TextField()

    labels = models.ManyToManyField(Label)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['slug'], name='unique_slug')
        ]
        ordering = ['title']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.markdown = MarkdownContainer(self)

    def __str__(self):
        return f'Recipe(title={self.title})'

    @property
    def cooktime_label(self):
        if self.cooktime > 59:
            hours = self.cooktime // 60
            minutes = hours * 60 - self.cooktime

            result = str(hours)
            if hours > 1:
                result += 's'

            if minutes:
                result += str(minutes)

            if minutes > 1:
                result += 's'

            return result

        return f'{self.cooktime} mins'
