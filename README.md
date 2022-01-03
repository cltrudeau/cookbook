# cookbook

This is the source for a static website containing my family's common recipes.

[https://cookbook.trudeau.dev](cookbook.trudeau.dev)

The content was formerly hosted using an OpenEats server, but that code is no
longer maintained and getting the data out was painful. Recipes have now been 
encoded in `.toml` files and the site is built using a small Django program in
combination with [django-distill](https://github.com/meeb/django-distill).

The site uses Joe Crawford's [https://github.com/joe-crawford/Static-Site-Search](Static-Site-Search)
tool.
