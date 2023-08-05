#############
pyApp - Redis
#############

*Let us handle the boring stuff!*

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/ambv/black
      :alt: Once you go Black...

This extension provides a `Redis` client factory to allow configuration to be
configured via pyApp settings.

The extension also provides checks to confirm the settings are correct and
that the application is able to connect to the redis instance.


Installation
============

Install using *pip*::

    pip install pyapp-redis

Install using *pipenv*::

    pipenv install pyapp-redis


Add `pae.redis` into the `EXT` list in your applications
`default_settings.py`.

Add the `REDIS` block into your runtime settings file::

    REDIS = {
        "default": {
            "url": "redis://user:pass@host:port/1",
        },
    }


.. note::

    The URL is a defined by Redis client see the
    `documentation <https://github.com/andymccurdy/redis-py/blob/master/redis/client.py#L599>`_.
    In addition to the url any argument that can be provided to `Redis.from_url` can be provided.


Usage
=====

The following example creates both `Connection` and `Session` instances::

    from pae.redis import get_client

    # Get connection
    redis = get_client()

    redis.set("foo")


API
===

`pae.redis.get_client(default: str = None) -> Redis`

    Get named `Redis` client instance
