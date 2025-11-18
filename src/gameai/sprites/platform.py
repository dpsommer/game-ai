from gameai import config

from .collision import CollidableObject2D


class Platform2D(CollidableObject2D):
    """Game surface such as platform or walls

    Args:
        settings (SurfaceOptions): configuration options for the surface
    """

    def __init__(self, settings: config.PlatformSettings):
        super(Platform2D, self).__init__(settings)
        self.friction_coefficient = settings.friction_coefficient
