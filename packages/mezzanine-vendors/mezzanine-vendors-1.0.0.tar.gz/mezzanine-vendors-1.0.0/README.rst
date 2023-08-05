
Mezzanine Vendors
=================

A Django / Mezzanine application to manage a vendor catalog. Features:

- CSV imports
- Uses the Google Maps API to determine coordinates from human-readable addresses
- Categorize vendors by service type and subject

Install
-------

1. Add your Google Maps API Key in your ``settings.py`` as ``GOOGLE_MAPS_API_KEY``
2. Install via pip: ``pip install mezzanine-vendors``.
3. Add ``vendors`` to your ``INSTALLED_APPS``.
4. Include ``vendors.urls`` in your root urlconf.
5. Run migrations.
6. Add Vendors using the admin interface.

**Note: This package provides the models, admin, and a JSON endpoint that returns the vendors. You'll need to create your own frontend to display them.**

Management Command
------------------

Run ``python manage.py add_vendor_locations`` to add coordinates to vendors that are missing them (for example, vendors added via admin import). This uses Google's GeoCoder API and will fail if the address cannot be parsed. It will also count towards the usage limit of your Google Maps API key.

Contributing
------------

Review contribution guidelines at CONTRIBUTING.md_.

.. _CONTRIBUTING.md: CONTRIBUTING.md
