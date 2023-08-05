==================
GLCS Web Interface
==================

`glcsweb` is a Django app which provides a web interface for the
`glcs` package. It requires `glcs` to be installed to work 
properly. 

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "glcsweb" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'polls',
    ]

2. Include the glcsweb URLconf in your project urls.py like this::

    path('/', include('glcsweb.urls')),

3. Run `python manage.py migrate` to create the glcsweb models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a  (you'll need the Admin app enabled).

5. Visit http://127.0.0.1:8000/polls/ to participate in the poll.