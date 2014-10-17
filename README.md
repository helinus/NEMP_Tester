A Python script that loads the relevant Check* function from NEMP_Class.py for every mod listed in ``mods``.
It is caching all web requests to the ``nemcache`` folder, if you need to fetch a fresh version of a file just delete it from that folder.

It needs the [NotEnoughMods](https://github.com/SinZ163/NotEnoughMods) repo to be cloned into the ``commands`` folder and an empty file named ``__init__.py`` (don't commit this file) in there.