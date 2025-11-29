import math
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.collections import LineCollection
from matplotlib.ticker import FuncFormatter

class GPS_Simulator:
    def __init__(self, lat, lon):
        """
        Initialize with starting point in degrees.
        """
        self.lat = lat
        self.lon = lon
        self.R = 6371000 # Earth radius in meters
        self.current_speed = 0
        self.current_heading = 0
        self.maneuvers = [] # List of (time, new_speed, new_heading)

    @staticmethod
    def _convert_to_mps(speed, unit):
        """
        Convert speed to meters per second.
        Supported units: 'm/s' 'kph', 'mph', 'knots', 'ft/s'
        """
        unit = unit.lower()
        if unit == 'm/s':
            return speed
        elif unit == 'kph':
            return speed / 3.6
        elif unit == 'mph':
            return speed * 0.44704
        elif unit == 'knots':
            return speed * 0.514444
        elif unit == 'ft/s':
            return speed * 0.3048
        else:
            raise ValueError(f"Unsupported unit: '{unit}'")


    def add_maneuver(self, time, speed=None, speed_unit='m/s', heading=None):
        """
        Schedule a maneuver at a given time (seconds).
        speed and heading are optional; if None, keep current.

        Speed can be specified in different units.
        """
        speed_m_s = None
        if speed is not None:
            speed_m_s = self._convert_to_mps(speed, speed_unit)

        self.maneuvers.append((time, speed_m_s, heading))
        # Ensure maneuvers are sorted by time
        self.maneuvers.sort(key=lambda x: x[0])

    def __apply_maneuvers(self, current_time):
        """
        Apply maneuvers scheduled at the current time.
        """
        while self.maneuvers and self.maneuvers[0][0] <= current_time:
            _, new_speed, new_heading = self.maneuvers.pop(0)
            if new_speed is not None:
                self.current_speed = new_speed
            if new_heading is not None:
                self.current_heading = new_heading

    def __move_one_step(self, dt):
        """
        Move the point for dt seconds based on current speed & heading.
        """
        lat1 = math.radians(self.lat)
        lon1 = math.radians(self.lon)
        heading = math.radians(self.current_heading)

        d = self.current_speed * dt

        lat2 = math.asin(
            math.sin(lat1) * math.cos(d / self.R) +
            math.cos(lat1) * math.sin(d / self.R) * math.cos(heading)
        )

        lon2 = lon1 + math.atan2(
            math.sin(heading) * math.sin(d / self.R) * math.cos(lat1),
            math.cos(d / self.R) - math.sin(lat1) * math.sin(lat2)
        )

        self.lat = math.degrees(lat2)
        self.lon = math.degrees(lon2)

        return self.lat, self.lon

    def simulate(self, end_time, dt=1):
        """
        Run the simulation until end_time (seconds), step size dt (seconds).
        Returns a list of (time, lat, lon).
        """

        results = []
        current_time = 0
        while current_time <= end_time:
            self.__apply_maneuvers(current_time)
            lat, lon = self.__move_one_step(dt)
            results.append((current_time, lat, lon))
            current_time += dt
        return results

    def track_plot(self, results, cmap='viridis'):
        """
        Plot lat vs lon with color gradient from start to end
        results: list of (time, lat, lon)
        cmap: any matplotlib colormap name (e.g. 'viridis', 'plasma', 'jet')
        """

        # Extract lat/lon
        lats = [r[1] for r in results]
        lons = [r[2] for r in results]

        # Create line segments
        points = np.array([lons, lats]).T.reshape(-1, 1, 2)
        segments = np.hstack([points[:-1], points[1:]])

        # Normalize time values 0 -> 1
        times = np.array([r[0] for r in results])
        norm = (times - times.min()) / (times.max() - times.min())

        # Create color-graded line collection
        lc = LineCollection(
                            segments,
                            cmap=cmap,
                            array=norm,
                            linewidths=3
                            )

        fig, ax = plt.subplots(figsize=(6,6))
        ax.add_collection(lc)

        # ----- Human-readable lat/lon formatting -----
        def format_lon(x, pos):
            """Format longitude with E/W suffix"""
            direction = 'E' if x >= 0 else 'W'
            return f"{abs(x):.5f}deg{direction}"

        def format_lat(x, pos):
            """Format latitude with N/S suffix"""
            direction = 'N' if x >= 0 else 'S'
            return f"{abs(x):.5f}deg{direction}"

        ax.xaxis.set_major_formatter(FuncFormatter(format_lon))
        ax.yaxis.set_major_formatter(FuncFormatter(format_lat))

        # Clean tick layout
        ax.set_xticks(np.linspace(min(lons), max(lons), 6))
        ax.set_yticks(np.linspace(min(lats), max(lats), 6))

        # Rotate X tick labels to 45
        plt.setp(ax.get_xticklabels(), rotation=45, ha='right')

        # ---------------------------------------------


        ax.set_xlabel("Longitude")
        ax.set_ylabel("Latitude")
        ax.set_title("Simulated GPS Track (Color-graded Start-End)")
        plt.grid(True)
        plt.axis("equal") # keep scale accurate


        # Add colorbar
        cbar = fig.colorbar(lc, ax=ax)
        cbar.set_label("Simulation Time (normalized)")

        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    # Example usage
    sim = GPS_Simulator(37.7749, -122.4194)
    #sim.current_speed = 5 # m/s
    sim.current_speed = GPS_Simulator._convert_to_mps(11.2, 'mph') # initial speed in mph
    sim.current_heading = 90 # degrees

    # Schedule maneuvers
    sim.add_maneuver(time=3, heading=45) # turn NE at t=3s
    sim.add_maneuver(time=6, speed=10, speed_unit='kph') # slow down at t=6s
    sim.add_maneuver(time=8, speed=15, speed_unit='knots')
    sim.add_maneuver(time=9, speed=10, speed_unit='ft/s', heading=48)
    sim.add_maneuver(time=15, speed=25, speed_unit='knots')
    sim.add_maneuver(time=20, speed=20, speed_unit='knots')
    sim.add_maneuver(time=35, speed=10, speed_unit='knots', heading=50)
    sim.add_maneuver(time=45, speed=2)

    # Run simulation for 10 seconds
    trajectory = sim.simulate(end_time=60)

    for t, lat, lon in trajectory:
        print(f"t={t:.0f}s -> lat={lat:.6f}, lon={lon:.6f}")

    sim.track_plot(trajectory)