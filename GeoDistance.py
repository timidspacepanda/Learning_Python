import math

class GeoDistance:
    """
    Class to calculate geographic distances using the Haversine formula.
    """

    def __init__(self, radius_km=6371):
        """
        Initialize the class with Earth's radius in kilometers. (default = 6371)
        """
        self.radius_km = radius_km

    def haversine(self, lat1, lon1, lat2, lon2, unit='km'):
        """
        Calculate the great-circle distance between two points on the Earth using the Haversine formula.

        Parameters:
            lat1, lon1: Latitude and Longitude of point 1 in decimal degrees.
            lat2, lon2: Latitude and Longitude of point 2 in decimal degrees.
            unit: 'km', 'm', 'mi', 'ft', or 'nmi' (nautical miles).
        Returns:
            Distance in the requested unit
        """
        # Convert decimal degrees to radians
        lat1_rad, lon1_rad = math.radians(lat1), math.radians(lon1)
        lat2_rad, lon2_rad = math.radians(lat2), math.radians(lon2)

        # Difference
        dlat = lat2_rad - lat1_rad
        dlon = lon2_rad - lon1_rad

        # Haversine formula
        a = (
            math.sin(dlat/2)**2 +
            math.cos(lat1_rad) *
            math.cos(lat2_rad) *
            math.sin(dlon/2)**2
        )
        c = 2 * math.asin(math.sqrt(a))

        distance_km = self.radius_km * c

        # Convert to request unit
        return self.__convert_unit(distance_km, unit)

    def haversine_points(self, point1, point2, unit='km'):
        """
        Wrapper function that accepts points as tuples (lat, lon)
        and calls the original haversine function.

        Parameters:
            point1: Latitude and Longitude of point 1 in decimal degrees.
            point2: Latitude and Longitude of point 2 in decimal degrees.
            unit: 'km', 'm', 'mi', 'ft', or 'nmi' (nautical miles).
        Returns:
            Distance in the requested unit
        """

        lat1, lon1 = point1
        lat2, lon2 = point2
        return self.haversine(lat1, lon1, lat2, lon2, unit)

    def __convert_unit(self, distance_km, unit):
        """
        Private method to convert distance in kilometers to other units.
        """

        unit = unit.lower()
        if unit == 'km':
            return distance_km
        elif unit == 'm':
            return distance_km * 1000
        elif unit == 'mi':
            return distance_km * 0.621371
        elif unit == 'ft':
            return distance_km * 3280.84
        elif unit == 'nmi':
            return distance_km * 0.539957
        else:
            raise ValueError(f"Unsupported unit: '{unit}'. Choose km, m, mi, ft, or nmi." )



if __name__ == "__main__":
    geo = GeoDistance()

    nyc = (40.7128, -74.0060)
    la = (34.0522, -118.2437)

    print(f"Distance (km): {geo.haversine(40.7128, -74.0060, 34.0522, -118.2437):.2f} km")
    print(f"Distance (m): {geo.haversine(40.7128, -74.0060, 34.0522, -118.2437, 'm'):.2f} m")
    print(f"Distance (mi): {geo.haversine(40.7128, -74.0060, 34.0522, -118.2437, 'mi'):.2f} mi")
    print(f"Distance (ft): {geo.haversine(40.7128, -74.0060, 34.0522, -118.2437, 'ft'):.2f} ft")
    print(f"Distance (nmi): {geo.haversine(40.7128, -74.0060, 34.0522, -118.2437, 'nmi'):.2f} nmi")
    print()
    print()
    print(f"Distance (km): {geo.haversine_points(nyc, la):.2f} km")
    print(f"Distance (m): {geo.haversine_points(nyc, la, 'm'):.2f} m")
    print(f"Distance (mi): {geo.haversine_points(nyc, la, 'mi'):.2f} mi")
    print(f"Distance (ft): {geo.haversine_points(nyc, la, 'ft'):.2f} ft")
    print(f"Distance (nmi): {geo.haversine_points(nyc, la, 'nmi'):.2f} nmi")