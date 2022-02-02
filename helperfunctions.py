from object_klasses import CelestialBody as CB


def planets_from_file(filename: str = "planeten.txt") -> list:
    solar_system_list = []  # Return object

    with open(filename) as f:

        for line in f:
            if line[0] != '#':  # Used for comments
                info = [i.replace(" ", "") for i in line[:-1].split(',')]  # Remove newline and spaces

                if len(info) == 4:  # Star
                    solar_system_list.append(CB(name=info[0], radius=float(info[1]), mass=float(info[2]), colour=info[3]
                                                ))

                if len(info) == 6:  # Planet
                    solar_system_list.append(CB(name=info[0], orbit_r=float(info[1]), radius=float(info[2]),
                                                mass=float(info[3]), v=float(info[4]), colour=info[5]
                                                ))

                if len(info) == 7:  # Moon
                    for celestial_body in reversed(solar_system_list):
                        if celestial_body.mother is None:
                            r = celestial_body.orbit_r
                            mother = celestial_body
                            break

                    solar_system_list.append(CB(name=info[1], orbit_r=float(info[2]), radius=float(info[3]),
                                                mass=float(info[4]), v=float(info[5]), colour=info[6],
                                                mother_radius=r, mother=mother
                                                ))

    return solar_system_list



