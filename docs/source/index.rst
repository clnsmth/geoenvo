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

`geoenvo` is a Python library that links geographic coordinates to environmental descriptions. It provides environmental descriptions in both the original format of the source data and a standardized ENVO ([Environment Ontology](https://sites.google.com/site/environmentontology/)) representation, mapping descriptions to ENVO terms for consistency and interoperability.

Motivation
----------

There is a vast amount of data available from diverse sources, and geoenvo offers a straightforward way to expose the environmental semantics of these datasets. By doing so, it provides a mechanism to connect otherwise disparate data sources through a shared environmental context, unlocking new opportunities for integrated analysis and research.

Quick Start
-----------

Install the current release from GitHub.

.. code-block:: bash

    pip install git+https://github.com/clnsmth/geoenvo.git@main

.. code-block:: python

    from json import dumps
    from geoenvo.resolvers.world_terrestrial_ecosystems import (
        WorldTerrestrialEcosystems,
    )
    from geoenvo.identifier import Identifier
    from geoenvo.geometry import Geometry

    # Create a geometry in GeoJSON format
    polygon_on_land = {
        "type": "Polygon",
        "coordinates": [
            [[-123.552, 39.804],
             [-120.83, 39.804],
             [-120.83, 40.441],
             [-123.552, 40.441],
             [-123.552, 39.804]]
        ]
    }
    geometry = Geometry(polygon_on_land)

    # Configure the identifier with one or more data sources
    identifier = Identifier(resolver=[WorldTerrestrialEcosystems()])

    # Identify the environment for the geometry and map to ENVO
    result = identifier.identify(
        geometry,
        identifier="5b4edec5-ea5e-471a-8a3c-2c1171d59dee",
        description="Polygon on land",
        vocabulary="ENVO"
    )

    # The result is a GeoJSON Feature with description and environment properties
    print(dumps(result.data, indent=2))


.. code-block:: json

    {
      "type": "Feature",
      "identifier": "5b4edec5-ea5e-471a-8a3c-2c1171d59dee",
      "geometry": {
        "type": "Polygon",
        "coordinates": [
          [
            [
              -123.552,
              39.804
            ],
            [
              -120.83,
              39.804
            ],
            [
              -120.83,
              40.441
            ],
            [
              -123.552,
              40.441
            ],
            [
              -123.552,
              39.804
            ]
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
              "resolver": "WorldTerrestrialEcosystems"
            },
            "dateCreated": "2025-02-14 11:51:57",
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


.. code-block:: python

    # The result can be converted to Schema.org JSON-LD
    schema_org = result.to_schema_org()
    print(dumps(schema_org, indent=2))


.. code-block:: json

    {
        "@context": "https://schema.org/",
        "@id": "5b4edec5-ea5e-471a-8a3c-2c1171d59dee",
        "@type": "Place",
        "description": "Polygon on land",
        "geo": {
            "@type": "GeoShape",
            "polygon": "39.804 -123.552 39.804 -120.83 40.441 -120.83 40.441 -123.552 39.804 -123.552"
        },
        "additionalProperty": [
            {
                "@type": "PropertyValue",
                "name": "Spatial reference system",
                "propertyID": "https://dbpedia.org/page/Spatial_reference_system",
                "value": "https://www.w3.org/2003/01/geo/wgs84_pos"
            },
            {
                "@type": "PropertyValue",
                "name": "temperature",
                "value": "Warm Temperate"
            },
            {
                "@type": "PropertyValue",
                "name": "moisture",
                "value": "Dry"
            },
            {
                "@type": "PropertyValue",
                "name": "landCover",
                "value": "Grassland"
            },
            {
                "@type": "PropertyValue",
                "name": "landForm",
                "value": "Plains"
            },
            {
                "@type": "PropertyValue",
                "name": "climate",
                "value": "Warm Temperate Dry"
            },
            {
                "@type": "PropertyValue",
                "name": "ecosystem",
                "value": "Warm Temperate Dry Grassland on Plains"
            }
        ],
        "keywords": [
            {
                "@id": "http://purl.obolibrary.org/obo/ENVO_01000206",
                "@type": "DefinedTerm",
                "name": "temperate",
                "inDefinedTermSet": "https://ontobee.org/ontology/ENVO",
                "termCode": "ENVO_01000206"
            },
            {
                "@id": "http://purl.obolibrary.org/obo/ENVO_01000230",
                "@type": "DefinedTerm",
                "name": "arid",
                "inDefinedTermSet": "https://ontobee.org/ontology/ENVO",
                "termCode": "ENVO_01000230"
            },
            {
                "@id": "http://purl.obolibrary.org/obo/ENVO_00000106",
                "@type": "DefinedTerm",
                "name": "grassland area",
                "inDefinedTermSet": "https://ontobee.org/ontology/ENVO",
                "termCode": "ENVO_00000106"
            },
            {
                "@id": "http://purl.obolibrary.org/obo/ENVO_00000086",
                "@type": "DefinedTerm",
                "name": "plain",
                "inDefinedTermSet": "https://ontobee.org/ontology/ENVO",
                "termCode": "ENVO_00000086"
            }
        ]
    }



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
