.. This README is meant for consumption by humans and PyPI. PyPI can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide.html
   This text does not appear on PyPI or github. It is a comment.

.. image:: https://github.com/collective/rer.linkmap/actions/workflows/plone-package.yml/badge.svg
    :target: https://github.com/collective/rer.linkmap/actions/workflows/plone-package.yml

.. image:: https://coveralls.io/repos/github/collective/rer.linkmap/badge.svg?branch=main
    :target: https://coveralls.io/github/collective/rer.linkmap?branch=main
    :alt: Coveralls

.. image:: https://codecov.io/gh/collective/rer.linkmap/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/collective/rer.linkmap

.. image:: https://img.shields.io/pypi/v/rer.linkmap.svg
    :target: https://pypi.python.org/pypi/rer.linkmap/
    :alt: Latest Version

.. image:: https://img.shields.io/pypi/status/rer.linkmap.svg
    :target: https://pypi.python.org/pypi/rer.linkmap
    :alt: Egg Status

.. image:: https://img.shields.io/pypi/pyversions/rer.linkmap.svg?style=plastic
    :alt: Supported - Python Versions

.. image:: https://img.shields.io/pypi/l/rer.linkmap.svg
    :target: https://pypi.python.org/pypi/rer.linkmap/
    :alt: License


============
RER Link map
============

"Amministrazione Trasparente" link map

Features
--------

- Control panel for configuring all transparency-map URLs.
- Dedicated outputs at portal root:
	- `at_map.json`
	- `at_map.xml`
- Independent flags to enable/disable JSON and XML exposure.
- REST API control panel integration (`linkmap-settings`).


Installation
------------

Install rer.linkmap by adding it to your buildout::

    [buildout]

    ...

    eggs =
        rer.linkmap


and then running ``bin/buildout``


Configuration
-------------

After installation, configure the add-on in:

- Site Setup -> Link map settings (`linkmap-settings`)

Main options:

- `expose_json`: enable/disable `@@at_map.json`
- `expose_xml`: enable/disable `@@at_map.xml`
- `data_ultima_modifica`: date string in `GG/MM/AAAA`
- one URL field for each transparency section key

If a format is disabled, the corresponding view returns `404 Not Found`.

Output Endpoints
----------------
Endpoints are available only on the portal root context:

- `/at_map.json`
- `/at_map.xml`

JSON example
------------

.. code-block:: json

    {
        "at_art2_bis_c1": {
            "amministrazione_trasparente": "https://www.example.org/amministrazione-trasparente",
            "disposizioni_generali": "https://www.example.org/disposizioni-generali"
        },
        "data_ultima_modifica": "17/06/2026"
    }

XML example
-----------

.. code-block:: xml

    <?xml version="1.0" encoding="utf-8"?>
    <amministrazione_trasparente xmlns="https://guida-servizi.anticorruzione.it/trasparenza">
        <data_ultima_modifica>18/06/2026</data_ultima_modifica>
        <map>
            <at_art2_bis_c1>
                <amministrazione_trasparente>https://www.example.org/at</amministrazione_trasparente>
                <accesso_civico>https://www.example.org/accesso-civico</accesso_civico>
            </at_art2_bis_c1>
        </map>
    </amministrazione_trasparente>

REST API Integration
--------------------


The add-on registers a restapi control panel adapter named
`linkmap-settings`, based on the same schema used by the classic control panel.

Credits
-------

Developed with the support of `Regione Emilia Romagna <http://www.regione.emilia-romagna.it>`_

Regione Emilia Romagna supports the `PloneGov initiative <http://www.plonegov.it>`_.

Authors
-------

This product was developed by **RedTurtle Technology** team.

Generated using `Cookieplone <https://github.com/plone/cookieplone>`_ and
`cookieplone-templates <https://github.com/plone/cookieplone-templates>`_.


License
-------

This project is licensed under the GPLv2.
