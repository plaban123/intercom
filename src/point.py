from math import radians

class Point(object):
    '''Represent a GPS point'''

    def __init__(self, lat_degrees=None, long_degrees=None, lat_radians=None, long_radians=None):

        if not ((lat_degrees and long_degrees) or (lat_radians and long_radians)):
            raise ValueError('Point object should be created with lat/long degrees or radian values')

        if lat_degrees and long_degrees:
            if not ((-90 <= lat_degrees <= 90) and (-180 <= long_degrees <= 180)):
                raise ValueError("Latitude/Longitude should range from [-90, -180] to [90, 180]")

        self.lat_degrees = lat_degrees
        self.long_degrees = long_degrees
        self.lat_radians = lat_radians
        self.long_radians = lat_radians

        if not self.lat_radians:
            self.set_radians()

    def set_radians(self):
        self.lat_radians, self.long_radians = map(radians, [self.lat_degrees, self.long_degrees])