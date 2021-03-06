from vpython import sphere, color, vector, canvas, norm, mag, rate
from math import pi, cos, sin
from random import randint
from time import sleep

COLOUR_SWITCH = {
    'yellow': color.yellow,
    'blue': color.blue,
    'red': color.red,
    'white': color.white,
    'orange': color.orange,
    'gray': color.gray(luminance=1)
}


class CelestialBody:
    """
    Python representation of celestial bodies (Stars, planets and satellites). Supports custom colour and name.
    Stars have an orbit radius of 0.
    Satellites take another CelestialBody as mother object.
    """

    def __init__(self, name: str, radius: float, mass: float, colour: str = color.white, v: float = 0,
                 orbit_r: float = 0, mother=None, mother_radius: float = 0, scaling: bool = False):
        """
        Creates a CelestialBody instance.
        @param name: Name of the body
        @param radius: Radius of the sphere representing the body
        @param mass: Mass of the body
        @param colour: Colour of the body, only single  colours are supported.
        @param v: Initial velocity of the body
        @param orbit_r: Orbit radius around the star. The star has an orbit radius of 0, does not have to be specified.
        @param mother: Orbiting body for a satellite.
        @param mother_radius: Orbit radius around the mother of the satellite.
        @param scaling: Scale radius up for better visibility. Recommended if there are very large differences in radia
         or large distances between bodies
        """
        self.name = name
        if scaling:
            if 0 < radius < 1000:
                self.r = radius * 100000000
            elif radius < 10000:
                self.r = radius * 1000000
            elif radius < 10000000:
                self.r = radius * 1000
            elif radius < 100000000:
                self.r = radius * 250
            else:
                self.r = radius * 50
        else:
            self.r = radius
        self.colour = colour
        self.mass = mass
        self.orbit_r = orbit_r
        self.v = v
        self.mother = mother
        self.mother_radius = mother_radius

        if scaling and self.mother:
            self.orbit_r += self.mother.r * 2

    def __str__(self):
        return_str = f'Celestial body: \n' \
                     f'Name: {self.name} \n' \
                     f'Radius: {self.r} \n' \
                     f'Orbital radius: {self.orbit_r} \n' \
                     f'Velocity: {self.v} ' \
                     f'Mass: {self.mass}, colour: {self.colour}'
        if self.mother:
            return_str += f'\nMother: {self.mother}'
        return return_str

    def __dict__(self):
        return {
            "name": self.name,
            "radius": self.r,
            "colour": self.colour,
            "mass": self.mass,
            "orbit radius": self.orbit_r,
            "velocity": self.v,
            "Mother": self.mother
        }


class StarSystem:
    """
    Star system composed of CelestialBody object. Based on the vpython library.
    Input is a list, first object will be used as the central force (I.e. star).
    A custom gravitational constant can be used, when different from newtons the movement will differ from reality.
    """

    def __init__(self, celestial_bodies: list, title: str, grav_constant: float = - 6.6742 * 10 ** (-11),
                 trailing: bool = False):
        """
        Creates the StarSystem instance. Build upon CelestialBody
        @param celestial_bodies: List of all CelestialBody's in the star system. The first item in the list
         will be the star.
        @param title: Title of the windows opened by vpython
        @param grav_constant: The gravitational constant of the universe. Will default to Newtons constant.
        @param trailing: Enable make_trail in vpython.sphere() instance. Satellites never have trails due
         to their unnatural movement.
        """
        bodies = []

        for body in celestial_bodies:
            body: CelestialBody
            if body.mother:
                obj = sphere(make_trail=False, color=COLOUR_SWITCH[body.colour], radius=body.r)
            else:
                obj = sphere(make_trail=trailing, color=COLOUR_SWITCH[body.colour], radius=body.r)

            obj.pos = vector(body.orbit_r + body.mother_radius, 0, 0)
            obj.p = body.mass * vector(0, body.v, 0)
            obj.celestial_body = body

            if body.mother:
                for celestial_body_sphere in reversed(bodies):
                    if celestial_body_sphere.mother is None:
                        obj.mother = celestial_body_sphere
                        break
            else:
                obj.mother = None

            if obj.mother:
                obj.n = randint(0, 50000)

            bodies.append(obj)

        self.celestial_bodies = bodies

        # Universal constants
        self.grav_constant = grav_constant
        self.star_mass = celestial_bodies[0].mass

        # Window:
        self.canvas = canvas(title=title, background=color.black)

    def move(self, dt: int, move_satellites: bool = False):
        """
        Move functions, iterates over all object but the star.
        @param dt: time moved
        @param move_satellites: Bool for enabling artificial satellite movement (circle)
        @return: None
        """
        for body in self.celestial_bodies[1::]:
            CB = body.celestial_body
            CB: CelestialBody

            if CB.mother and move_satellites:
                n = body.n - body.n % 100
                body.pos = body.mother.pos + vector(CB.orbit_r * cos(n * pi / 50000),
                                                    CB.orbit_r * sin(n * pi / 50000), 0)

                body.n += 1
            else:
                F = self.grav_constant * self.star_mass * CB.mass * norm(body.pos) / mag(body.pos) ** 2
                body.p += F * dt
                body.pos += body.p * dt / CB.mass

    def start(self, n: int, dt: int, move_satellites: bool = False):
        """
        Start movement of the star system
        @param n: Amount of times the time passes
        @param dt: Amount of time that passes per movement update (*1000 due to vpython.rate())
        @param move_satellites: Bool for enabling artificial satellite movement (circle)
        @return: None
        """
        t = 0

        sleep(5)

        while t < n:
            rate(1000)
            self.move(dt, move_satellites=move_satellites)

            t += 1
