from helperfunctions import planets_from_file
from object_klasses import StarSystem


def main():
    solar_system = StarSystem(planets_from_file(scaling=True), "Our Solar System", trailing=True)

    solar_system.start(24 * 60 * 60, 60, move_satellites=True)


if __name__ == '__main__':
    main()
