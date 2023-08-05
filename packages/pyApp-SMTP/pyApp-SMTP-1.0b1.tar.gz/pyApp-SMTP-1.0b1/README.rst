############
pyApp - SMTP
############

*Let us handle the boring stuff!*

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: http://github.com/ambv/black
   :alt: Once you go Black...

This extension provides an `SMTP` client object configured via pyApp settings.


Installation
============

Install using *pip*::

    pip install pyApp-SMTP

Install using *pipenv*::

    pip install pyApp-SMTP


Add `pae.smtp` into the `EXT` list in your applications `default_settings.py`.

Add the `SMTP` block into your runtime settings file::

    SMTP = {
        "default": {
            "host": "localhost",
        }
    }


.. note::

    In addition to the *host* any argument that can be provided to `smtplib.SMTP` can be
    provided.


Usage
=====

The following example creates an SMTP client instance::

    from pae.smtp import get_client

    smtp = get_client()


API
===

`pae.smtp.get_client() -> SMTP`

    Get named `SMTP` instance.

