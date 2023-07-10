How to localize text in django
---
> #### Firstly add in templates header:
> ```html
> {% load i18n %}
> {% trans 'Some text' %}
> or:
> {% translate 'Some text' %}
>```
> #### Create new folder "locale" in app's folder.
> #### After that collect all text to translate with command:
> ```commandline
> django-admin makemessages -l ru
>```
> #### This command will create in "locale" folder file with all text to translate.
> #### It needs to be translated and after that compile all changes with command:
> ```commandline
> django-admin compilemessages
>```
> #### If you need to switch site language according client language add this line in settings middleware after CommonMiddleware:
> ```python
> 'django.middleware.locale.LocaleMiddleware',
> ```
---