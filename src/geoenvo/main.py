"""The main2 module"""

from geoenvo.identifier import Identifier
from geoenvo.data_sources import EcologicalCoastalUnits
from geoenvo.data_sources import EcologicalMarineUnits
from geoenvo.data_sources import WorldTerrestrialEcosystems
from geoenvo.environment import Environment

if __name__ == "__main__":

    # Configure
    geometry = "5"  # TODO: Update this script to use a real geometry
    data_sources = [
        WorldTerrestrialEcosystems(),
        EcologicalCoastalUnits(),
        EcologicalMarineUnits(),
    ]
    identifier = Identifier(data_sources)

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
