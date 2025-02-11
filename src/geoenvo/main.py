"""The main2 module"""

from geoenvo.identifier import Identifier
from geoenvo.resolvers.ecological_coastal_units import EcologicalCoastalUnits
from geoenvo.resolvers.ecological_marine_units import EcologicalMarineUnits
from geoenvo.resolvers.world_terrestrial_ecosystems import WorldTerrestrialEcosystems
from geoenvo.environment import Environment

if __name__ == "__main__":

    # Configure
    geometry = "5"  # TODO: Update this script to use a real geometry
    resolvers = [
        WorldTerrestrialEcosystems(),
        EcologicalCoastalUnits(),
        EcologicalMarineUnits(),
    ]
    identifier = Identifier(resolvers)

    # Resolve
    environment = identifier.identify(geometry)
    print(f"Identification returned: {environment.data}")

    # Set vocabulary terms (optional)
    environment.apply_vocabulary("ENVO")
    print(f"Set vocabulary terms returned: {environment.data}")

    # Write to file
    environment.write_data("/Users/me/data")

    # Read from file
    environment = Environment()
    environment.read_data("/Users/me/data/file.json")
    print(environment.data)
