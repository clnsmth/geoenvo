# geoenvo

[![Project Status: WIP – Initial development is in progress, but there has not yet been a stable, usable release suitable for the public.](https://www.repostatus.org/badges/latest/wip.svg)](https://www.repostatus.org/#wip)
![example workflow](https://github.com/clnsmth/geoenvo/actions/workflows/ci-cd.yml/badge.svg)
[![codecov](https://codecov.io/github/clnsmth/geoenvo/graph/badge.svg?token=2J4MNIXCTD)](https://codecov.io/github/clnsmth/geoenvo)

`geoenvo` is a Python library that links geographic coordinates to environmental properties at a global scale. These properties are described using the terminology of the source data, with options to map to other semantic resources, including controlled vocabularies and ontologies. By default, `geoenvo` maps to ENVO ([Environment Ontology](https://sites.google.com/site/environmentontology/)).

If you know of a **data source, vocabulary, or ontology** 
that could enhance this effort, please share it—even if it overlaps with existing resources.

## Motivation

There is a vast amount of data available from diverse sources, and geoenvo offers a straightforward way to expose the environmental semantics of these datasets. By doing so, it provides a mechanism to connect otherwise disparate data sources through a shared environmental context, unlocking new opportunities for integrated analysis and research.

## Quick Start

Install the current release from GitHub.

```bash
pip install git+https://github.com/clnsmth/geoenvo.git@main
```

Resolve a geometry to its environment(s).

```python
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

```

The response is a GeoJSON feature containing a list of environments and their associated properties. These properties map to semantic resources, ENVO by default.

```json
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


```


Format the response as Schema.org.

```python
schema_org = response.to_schema_org()
```



