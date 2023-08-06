============================
snippet-image
============================

Package for simple creation images of snippets for social networks using pillow_.

.. _pillow: https://pillow.readthedocs.io/en/stable/

Pictures for snippets can be inserted for sharing pages in social networks, for example in tag meta:

.. code-block:: html

    <meta property="og:image" content="Link to your snippet image" />
    <meta name="twitter:image" content="Link to your snippet image" />

Installation
---------------------------

`pip3 install snippet-image`

User guide
---------------------------

To start creating images for snippets, it is enough to import the function ```from snippet_image import create_snippet_image```.

.. code-block:: python

    from snippet_image import create_snippet_image

    image_blob = create_snippet_image(
            font='/home/iamterminator/.fonts/OpenSans-Bold.ttf', # Path to your font file
            font_size=62, # Font size
            background='/home/iamterminator/.wallpapers/jakethedog.jpg', # Path to your background image
            size=(1200, 630), # Size of snippet image. (width, height)
            text='Jake the Dog', # Text for draw on snippet image
            brightness=0.3, # Brightness of background
        )

    with open('jake-the-dog-snippet-image.jpg', 'wb') as file:
        file.write(image_blob.getvalue())

Integration
--------------------

Django: `django-snippet-image`_.

Wagtail: `wagtail-snippet-image`_.

.. _django-snippet-image: https://github.com/acrius/django-snippet-image

.. _wagtail-snippet-image: https://github.com/acrius/wagtail-snippet-image

Read more on home_.

.. _home: https://github.com/acrius/snippet-image.
