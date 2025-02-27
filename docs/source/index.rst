Welcome to `geoenvo`
====================

Release v\ |version|. (:ref:`Installation <quickstart>`)

.. image:: https://www.repostatus.org/badges/latest/wip.svg
    :target: https://www.repostatus.org/#wip
    :alt: Project Status: WIP – Initial development is in progress, but there has not yet been a stable, usable release suitable for the public.

.. image:: https://github.com/clnsmth/geoenvo/actions/workflows/ci-cd.yml/badge.svg
    :target: https://github.com/clnsmth/geoenvo/actions/workflows/ci-cd.yml
    :alt: CI/CD pipeline status

.. image:: https://codecov.io/github/clnsmth/geoenvo/graph/badge.svg?token=2J4MNIXCTD
    :target: https://codecov.io/github/clnsmth/geoenvo
    :alt: Code coverage status

`geoenvo` is a Python library that links geographic coordinates to environmental properties. These properties are described using the terminology of the source data, with options to map to other semantic resources, including controlled vocabularies and ontologies. By default, `geoenvo` maps to ENVO (`Environment Ontology`_).

.. _Environment Ontology: https://sites.google.com/site/environmentontology/

Motivation
----------

There is a vast amount of data available from diverse sources, and geoenvo offers a straightforward way to expose the environmental semantics of these datasets. By doing so, it provides a mechanism to connect otherwise disparate data sources through a shared environmental context, unlocking new opportunities for integrated analysis and research.

Quick Start
-----------

Install the current release from GitHub.

.. code-block:: bash

    pip install git+https://github.com/clnsmth/geoenvo.git@main

Resolve a geometry to its environment(s).

.. code-block:: python

    from json import dumps
    from geoenvo.data_sources import WorldTerrestrialEcosystems
    from geoenvo.resolver import Resolver
    from geoenvo.geometry import Geometry

    # Create a geometry in GeoJSON format
    polygon_on_land = {
        "type": "Polygon",
        "coordinates": [
            [
                [-123.552, 39.804],
                [-120.83, 39.804],
                [-120.83, 40.441],
                [-123.552, 40.441],
                [-123.552, 39.804],
            ]
        ],
    }
    geometry = Geometry(polygon_on_land)

    # Configure the resolver with one or more data sources
    resolver = Resolver(data_source=[WorldTerrestrialEcosystems()])

    # Resolve the geometry to environmental descriptions
    response = resolver.resolve(
        geometry,
        identifier="5b4edec5-ea5e-471a-8a3c-2c1171d59dee",
        description="Polygon on land",
    )

The response is a GeoJSON Feature containing a list of environments and their associated properties. These properties map to semantic resources, ENVO by default.

.. code-block:: json

    {
      "type": "Feature",
      "identifier": "5b4edec5-ea5e-471a-8a3c-2c1171d59dee",
      "geometry": {
        "type": "Polygon",
        "coordinates": [
            [
                [-123.552, 39.804],
                [-120.83, 39.804],
                [-120.83, 40.441],
                [-123.552, 40.441],
                [-123.552, 39.804]
            ]
        ]
      },
      "properties": {
        "description": "Polygon on land",
        "environment": [
          {
            "type": "Environment",
            "dataSource": {
              "identifier": "https://doi.org/10.5066/P9DO61LP",
              "name": "WorldTerrestrialEcosystems"
            },
            "dateCreated": "2025-02-18 08:27:46",
            "properties": {
              "temperature": "Warm Temperate",
              "moisture": "Dry",
              "landCover": "Grassland",
              "landForm": "Plains",
              "climate": "Warm Temperate Dry",
              "ecosystem": "Warm Temperate Dry Grassland on Plains"
            },
            "mappedProperties": [
              {
                "label": "temperate",
                "uri": "http://purl.obolibrary.org/obo/ENVO_01000206"
              },
              {
                "label": "arid",
                "uri": "http://purl.obolibrary.org/obo/ENVO_01000230"
              },
              {
                "label": "grassland area",
                "uri": "http://purl.obolibrary.org/obo/ENVO_00000106"
              },
              {
                "label": "plain",
                "uri": "http://purl.obolibrary.org/obo/ENVO_00000086"
              }
            ]
          }
        ]
      }
    }


Format the response as Schema.org.

.. code-block:: python

    schema_org = response.to_schema_org()




The API Documentation / Guide
-----------------------------

If you are looking for information on a specific function, class, or method,
this part of the documentation is for you.

.. toctree::
   :maxdepth: 2

   user/api


The Contributor Guide
---------------------

If you want to contribute to the project, this part of the documentation is for
you.

.. toctree::
   :maxdepth: 3

   dev/contributing

The Maintainer Guide
--------------------

If you are a project maintainer, this part of the documentation is for
you.

.. toctree::
   :maxdepth: 3

   dev/maintaining

Project Design
--------------

The project design documentation provides an overview of the project's
architecture and design decisions.

.. toctree::
   :maxdepth: 3

   dev/design
