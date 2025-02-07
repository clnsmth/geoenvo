"""The main2 module"""

from spinneret.identifier import Identifier
from spinneret.resolvers.ecological_coastal_units import EcologicalCoastalUnits
from spinneret.resolvers.ecological_marine_units import EcologicalMarineUnits
from spinneret.resolvers.world_terrestrial_ecosystems import WorldTerrestrialEcosystems
from spinneret.environment import Environment

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
    print(f"Identification returned: {environment.data()}")

    # Set vocabulary terms (optional)
    environment.apply_vocabulary("ENVO")
    print(f"Set vocabulary terms returned: {environment.data()}")

    # Write to file
    environment.write_data("/Users/me/data")

    # Read from file
    environment = Environment()
    environment.read_data("/Users/me/data/file.json")
    print(environment.data())
