# geoenvo

[![Project Status: WIP – Initial development is in progress, but there has not yet been a stable, usable release suitable for the public.](https://www.repostatus.org/badges/latest/wip.svg)](https://www.repostatus.org/#wip)
![example workflow](https://github.com/clnsmth/geoenvo/actions/workflows/ci-cd.yml/badge.svg)
[![codecov](https://codecov.io/github/clnsmth/geoenvo/graph/badge.svg?token=2J4MNIXCTD)](https://codecov.io/github/clnsmth/geoenvo)

`geoenvo` is a Python library that links geographic coordinates to environmental descriptions. It provides environmental descriptions in both the original format of the source data and a standardized ENVO ([Environment Ontology](https://sites.google.com/site/environmentontology/)) representation, mapping descriptions to ENVO terms for consistency and interoperability.

## Motivation

There is a vast amount of data available from diverse sources, and geoenvo offers a straightforward way to expose the environmental semantics of these datasets. By doing so, it provides a mechanism to connect otherwise disparate data sources through a shared environmental context, unlocking new opportunities for integrated analysis and research. 

## Quick Start

Install the current release from GitHub.

```bash
pip install git+https://github.com/clnsmth/geoenvo.git@main
```

```python
from json import dumps
from geoenvo.resolvers.world_terrestrial_ecosystems import \
    WorldTerrestrialEcosystems
from geoenvo.resolvers.ecological_marine_units import \
    EcologicalMarineUnits
from geoenvo.resolvers.ecological_coastal_units import \
    EcologicalCoastalUnits
from geoenvo.identifier import Identifier
from geoenvo.geometry import Geometry

# Create a geometry in GeoJSON format
# polygon_on_land_and_ocean = load_geometry(
#     "polygon_on_land_and_ocean_example")
polygon_on_land_and_ocean = {
    "type": "Polygon",
    "coordinates": [
        [[-123.716239, 39.325978],
         [-123.8222818, 39.3141049],
         [-123.8166231, 39.2943269],
         [-123.716239, 39.325978]]
    ]
}
geometry = Geometry(polygon_on_land_and_ocean)

# Configure the identifier with data sources to query
identifier = Identifier(
    resolver=[
        WorldTerrestrialEcosystems(),
        EcologicalMarineUnits(),
        EcologicalCoastalUnits()
    ]
)

# Identify the environment for the geometry
result = identifier.identify(geometry)

# The result is a JSON object
print(dumps(result._data, indent=2))


```

```json
{
    "type": "Feature",
    "identifier": "A polygon on land and ocean",
    "geometry": {
        "type": "Polygon",
        "coordinates": [
            [
                [
                    -123.716239,
                    39.325978
                ],
                [
                    -123.8222818,
                    39.3141049
                ],
                [
                    -123.8166231,
                    39.2943269
                ],
                [
                    -123.716239,
                    39.325978
                ]
            ]
        ]
    },
    "properties": {
        "environment": [
            {
                "type": "Environment",
                "dataSource": {
                    "identifier": "https://doi.org/10.5066/P9DO61LP",
                    "resolver": "WorldTerrestrialEcosystems"
                },
                "dateCreated": "2025-02-06 10:07:17",
                "properties": {
                    "temperature": "Warm Temperate",
                    "moisture": "Moist",
                    "landCover": "Forest",
                    "landForm": "Mountains",
                    "climate": "Warm Temperate Moist",
                    "ecosystem": "Warm Temperate Moist Forest on Mountains"
                },
                "envoTerms": [
                    {
                        "label": "temperate",
                        "uri": "http://purl.obolibrary.org/obo/ENVO_01000206"
                    },
                    {
                        "label": "humid air",
                        "uri": "http://purl.obolibrary.org/obo/ENVO_01000828"
                    },
                    {
                        "label": "forested area",
                        "uri": "http://purl.obolibrary.org/obo/ENVO_00000111"
                    },
                    {
                        "label": "mountain range",
                        "uri": "http://purl.obolibrary.org/obo/ENVO_00000080"
                    }
                ]
            },
            {
                "type": "Environment",
                "dataSource": {
                    "identifier": "https://doi.org/10.5066/P9Q6ZSGN",
                    "resolver": "EcologicalMarineUnits"
                },
                "dateCreated": "2025-02-06 10:07:17",
                "properties": {
                    "oceanName": "North Pacific",
                    "depth": "Epipelagic",
                    "temperature": "Cold",
                    "salinity": "Euhaline",
                    "dissolvedOxygen": "Oxic",
                    "nitrate": "Medium Nitrate",
                    "phosphate": "Low Phosphate",
                    "silicate": "Low Silicate",
                    "ecosystem": "North Pacific, Epipelagic, Cold, Euhaline, Oxic, Medium Nitrate, Low Phosphate, Low Silicate"
                },
                "envoTerms": [
                    {
                        "label": "North Pacific Ocean",
                        "uri": "http://purl.obolibrary.org/obo/GAZ_00002410"
                    },
                    {
                        "label": "marine photic zone",
                        "uri": "http://purl.obolibrary.org/obo/ENVO_00000209"
                    },
                    {
                        "label": "oxic water",
                        "uri": "http://purl.obolibrary.org/obo/ENVO_01001063"
                    },
                    {
                        "label": "oxic water",
                        "uri": "http://purl.obolibrary.org/obo/ENVO_01001063"
                    }
                ]
            },
            {
                "type": "Environment",
                "dataSource": {
                    "identifier": "https://doi.org/10.5066/P9Q6ZSGN",
                    "resolver": "EcologicalMarineUnits"
                },
                "dateCreated": "2025-02-06 10:07:17",
                "properties": {
                    "oceanName": "North Pacific",
                    "depth": "Epipelagic",
                    "temperature": "Very Cold",
                    "salinity": "Euhaline",
                    "dissolvedOxygen": "Oxic",
                    "nitrate": "Medium Nitrate",
                    "phosphate": "Low Phosphate",
                    "silicate": "Low Silicate",
                    "ecosystem": "North Pacific, Epipelagic, Very Cold, Euhaline, Oxic, Medium Nitrate, Low Phosphate, Low Silicate"
                },
                "envoTerms": [
                    {
                        "label": "North Pacific Ocean",
                        "uri": "http://purl.obolibrary.org/obo/GAZ_00002410"
                    },
                    {
                        "label": "marine photic zone",
                        "uri": "http://purl.obolibrary.org/obo/ENVO_00000209"
                    },
                    {
                        "label": "oxic water",
                        "uri": "http://purl.obolibrary.org/obo/ENVO_01001063"
                    },
                    {
                        "label": "oxic water",
                        "uri": "http://purl.obolibrary.org/obo/ENVO_01001063"
                    }
                ]
            },
            {
                "type": "Environment",
                "dataSource": {
                    "identifier": "https://doi.org/10.5066/P9HWHSPU",
                    "resolver": "EcologicalCoastalUnits"
                },
                "dateCreated": "2025-02-06 10:07:17",
                "properties": {
                    "slope": "steeply sloping",
                    "sinuosity": "sinuous",
                    "erodibility": "medium erodibility",
                    "temperatureAndMoistureRegime": "warm temperate moist",
                    "riverDischarge": "moderate river discharge",
                    "waveHeight": "moderate wave energy",
                    "tidalRange": "moderately tidal",
                    "marinePhysicalEnvironment": "euhaline-oxic-very cold",
                    "turbidity": "moderately turbid",
                    "chlorophyll": "low chlorophyll",
                    "ecosystem": "steeply sloping, sinuous, medium erodibility, warm temperate moist, moderate river discharge, moderate wave energy, moderately tidal, euhaline-oxic-very cold, moderately turbid, low chlorophyll"
                },
                "envoTerms": [
                    {
                        "label": "sloped",
                        "uri": "http://purl.obolibrary.org/obo/PATO_0001481"
                    },
                    {
                        "label": "undulate",
                        "uri": "http://purl.obolibrary.org/obo/PATO_0000967"
                    },
                    {
                        "label": "oligotrophic water",
                        "uri": "https://w3id.org/sssom/NoMapping"
                    },
                    {
                        "label": "oligotrophic water",
                        "uri": "https://w3id.org/sssom/NoMapping"
                    }
                ]
            },
            {
                "type": "Environment",
                "dataSource": {
                    "identifier": "https://doi.org/10.5066/P9HWHSPU",
                    "resolver": "EcologicalCoastalUnits"
                },
                "dateCreated": "2025-02-06 10:07:17",
                "properties": {
                    "slope": "sloping",
                    "sinuosity": "sinuous",
                    "erodibility": "high erodibility",
                    "temperatureAndMoistureRegime": "warm temperate moist",
                    "riverDischarge": "moderate river discharge",
                    "waveHeight": "moderate wave energy",
                    "tidalRange": "moderately tidal",
                    "marinePhysicalEnvironment": "euhaline-oxic-very cold",
                    "turbidity": "moderately turbid",
                    "chlorophyll": "low chlorophyll",
                    "ecosystem": "sloping, sinuous, high erodibility, warm temperate moist, moderate river discharge, moderate wave energy, moderately tidal, euhaline-oxic-very cold, moderately turbid, low chlorophyll"
                },
                "envoTerms": [
                    {
                        "label": "sloped",
                        "uri": "http://purl.obolibrary.org/obo/PATO_0001481"
                    },
                    {
                        "label": "undulate",
                        "uri": "http://purl.obolibrary.org/obo/PATO_0000967"
                    },
                    {
                        "label": "oligotrophic water",
                        "uri": "https://w3id.org/sssom/NoMapping"
                    },
                    {
                        "label": "oligotrophic water",
                        "uri": "https://w3id.org/sssom/NoMapping"
                    }
                ]
            },
            {
                "type": "Environment",
                "dataSource": {
                    "identifier": "https://doi.org/10.5066/P9HWHSPU",
                    "resolver": "EcologicalCoastalUnits"
                },
                "dateCreated": "2025-02-06 10:07:17",
                "properties": {
                    "slope": "sloping",
                    "sinuosity": "straight",
                    "erodibility": "high erodibility",
                    "temperatureAndMoistureRegime": "warm temperate moist",
                    "riverDischarge": "moderate river discharge",
                    "waveHeight": "moderate wave energy",
                    "tidalRange": "moderately tidal",
                    "marinePhysicalEnvironment": "euhaline-oxic-very cold",
                    "turbidity": "moderately turbid",
                    "chlorophyll": "low chlorophyll",
                    "ecosystem": "sloping, straight, high erodibility, warm temperate moist, moderate river discharge, moderate wave energy, moderately tidal, euhaline-oxic-very cold, moderately turbid, low chlorophyll"
                },
                "envoTerms": [
                    {
                        "label": "sloped",
                        "uri": "http://purl.obolibrary.org/obo/PATO_0001481"
                    },
                    {
                        "label": "straight",
                        "uri": "http://purl.obolibrary.org/obo/PATO_0002180"
                    },
                    {
                        "label": "oligotrophic water",
                        "uri": "https://w3id.org/sssom/NoMapping"
                    },
                    {
                        "label": "oligotrophic water",
                        "uri": "https://w3id.org/sssom/NoMapping"
                    }
                ]
            },
            {
                "type": "Environment",
                "dataSource": {
                    "identifier": "https://doi.org/10.5066/P9HWHSPU",
                    "resolver": "EcologicalCoastalUnits"
                },
                "dateCreated": "2025-02-06 10:07:17",
                "properties": {
                    "slope": "steeply sloping",
                    "sinuosity": "sinuous",
                    "erodibility": "high erodibility",
                    "temperatureAndMoistureRegime": "warm temperate moist",
                    "riverDischarge": "moderate river discharge",
                    "waveHeight": "moderate wave energy",
                    "tidalRange": "moderately tidal",
                    "marinePhysicalEnvironment": "euhaline-oxic-very cold",
                    "turbidity": "moderately turbid",
                    "chlorophyll": "low chlorophyll",
                    "ecosystem": "steeply sloping, sinuous, high erodibility, warm temperate moist, moderate river discharge, moderate wave energy, moderately tidal, euhaline-oxic-very cold, moderately turbid, low chlorophyll"
                },
                "envoTerms": [
                    {
                        "label": "sloped",
                        "uri": "http://purl.obolibrary.org/obo/PATO_0001481"
                    },
                    {
                        "label": "undulate",
                        "uri": "http://purl.obolibrary.org/obo/PATO_0000967"
                    },
                    {
                        "label": "oligotrophic water",
                        "uri": "https://w3id.org/sssom/NoMapping"
                    },
                    {
                        "label": "oligotrophic water",
                        "uri": "https://w3id.org/sssom/NoMapping"
                    }
                ]
            },
            {
                "type": "Environment",
                "dataSource": {
                    "identifier": "https://doi.org/10.5066/P9HWHSPU",
                    "resolver": "EcologicalCoastalUnits"
                },
                "dateCreated": "2025-02-06 10:07:17",
                "properties": {
                    "slope": "sloping",
                    "sinuosity": "sinuous",
                    "erodibility": "high erodibility",
                    "temperatureAndMoistureRegime": "warm temperate moist",
                    "riverDischarge": "moderate river discharge",
                    "waveHeight": "moderate wave energy",
                    "tidalRange": "moderately tidal",
                    "marinePhysicalEnvironment": "euhaline-oxic-very cold",
                    "turbidity": "moderately turbid",
                    "chlorophyll": "moderate chlorophyll",
                    "ecosystem": "sloping, sinuous, high erodibility, warm temperate moist, moderate river discharge, moderate wave energy, moderately tidal, euhaline-oxic-very cold, moderately turbid, moderate chlorophyll"
                },
                "envoTerms": [
                    {
                        "label": "sloped",
                        "uri": "http://purl.obolibrary.org/obo/PATO_0001481"
                    },
                    {
                        "label": "undulate",
                        "uri": "http://purl.obolibrary.org/obo/PATO_0000967"
                    },
                    {
                        "label": "mesotrophic water",
                        "uri": "https://w3id.org/sssom/NoMapping"
                    },
                    {
                        "label": "mesotrophic water",
                        "uri": "https://w3id.org/sssom/NoMapping"
                    }
                ]
            },
            {
                "type": "Environment",
                "dataSource": {
                    "identifier": "https://doi.org/10.5066/P9HWHSPU",
                    "resolver": "EcologicalCoastalUnits"
                },
                "dateCreated": "2025-02-06 10:07:17",
                "properties": {
                    "slope": "sloping",
                    "sinuosity": "sinuous",
                    "erodibility": "medium erodibility",
                    "temperatureAndMoistureRegime": "warm temperate moist",
                    "riverDischarge": "moderate river discharge",
                    "waveHeight": "moderate wave energy",
                    "tidalRange": "moderately tidal",
                    "marinePhysicalEnvironment": "euhaline-oxic-very cold",
                    "turbidity": "moderately turbid",
                    "chlorophyll": "low chlorophyll",
                    "ecosystem": "sloping, sinuous, medium erodibility, warm temperate moist, moderate river discharge, moderate wave energy, moderately tidal, euhaline-oxic-very cold, moderately turbid, low chlorophyll"
                },
                "envoTerms": [
                    {
                        "label": "sloped",
                        "uri": "http://purl.obolibrary.org/obo/PATO_0001481"
                    },
                    {
                        "label": "undulate",
                        "uri": "http://purl.obolibrary.org/obo/PATO_0000967"
                    },
                    {
                        "label": "oligotrophic water",
                        "uri": "https://w3id.org/sssom/NoMapping"
                    },
                    {
                        "label": "oligotrophic water",
                        "uri": "https://w3id.org/sssom/NoMapping"
                    }
                ]
            }
        ]
    }
}

```
