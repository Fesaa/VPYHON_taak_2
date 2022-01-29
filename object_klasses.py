from vpython import sphere, color, vector, canvas, norm, mag, rate

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
    Satellites take an other CelestialBody as mother object.
    """

    def __init__(self, name: str, radius: float, mass: float, colour: str, v: float = 0, orbit_r: float = 0,
                 mother: str = None, mother_radius: float = 0):
        self.name = str(name)
        self.r = float(radius)
        self.colour = colour
        self.mass = float(mass)
        self.orbit_r = float(orbit_r)
        self.v = float(v)
        self.mother = mother
        self.mother_radius = float(mother_radius)

    def __str__(self):
        return_str = f'Celestial body: \n' \
                     f'Name: {self.name} \n' \
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

    def __init__(self, celestial_bodies: list, title: str, grav_constant: float = - 6.6742 * 10 ** (-11)):
        bodies = []

        for body in celestial_bodies:
            body: CelestialBody
            obj = sphere(make_trail=True, color=COLOUR_SWITCH[body.colour], radius=body.r)
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

            bodies.append(obj)

        self.celestial_bodies = bodies

        # Universal constants
        self.grav_constant = grav_constant
        self.star_mass = celestial_bodies[0].mass

        # Window:
        self.canvas = canvas(title=title, background=color.black)

    def move(self, dt):

        for body in self.celestial_bodies[1::]:
            CB = body.celestial_body
            CB: CelestialBody

            if CB.mother:
                body.pos = body.mother.pos + vector(0, CB.orbit_r, 0)
            else:
                F = self.grav_constant * self.star_mass * CB.mass * norm(body.pos) / mag(body.pos) ** 2
                body.p += F * dt
                body.pos += body.p * dt / CB.mass

    def start(self, n, dt):
        t = 0

        while t < n:
            rate(1000)
            self.move(dt)

            t += 1

        print("Movement has ended.")
