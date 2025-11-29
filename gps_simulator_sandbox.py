from gps_simulator import GPS_Simulator
from geo_distance import GeoDistance

sim = GPS_Simulator(37.7749, -122.4194)
sim.current_speed = GPS_Simulator._convert_to_mps(5, 'knots') # initial speed in mph
sim.current_heading = 90 # degrees

# Schedule maneuvers
sim.add_maneuver(time=3, heading=45) # turn NE at t=3s
sim.add_maneuver(time=6, speed=5, speed_unit='knots') # slow down at t=6s
sim.add_maneuver(time=8, speed=15, speed_unit='knots')
sim.add_maneuver(time=9, speed=20, speed_unit='knots', heading=48)
sim.add_maneuver(time=15, speed=25, speed_unit='knots')
sim.add_maneuver(time=20, speed=20, speed_unit='knots')
sim.add_maneuver(time=35, speed=10, speed_unit='knots', heading=50)
sim.add_maneuver(time=45, speed=2, speed_unit='knots', heading=55)
sim.add_maneuver(time=60, speed=30, speed_unit='knots', heading=60)
sim.add_maneuver(time=65, speed=15, speed_unit='knots', heading=65)
sim.add_maneuver(time=70, speed=10, speed_unit='knots', heading=70)
sim.add_maneuver(time=75, speed=5, speed_unit='knots', heading=85)
sim.add_maneuver(time=80, speed=5, speed_unit='knots', heading=90)
sim.add_maneuver(time=90, speed=5, speed_unit='knots', heading=100)
sim.add_maneuver(time=100, speed=3, speed_unit='knots', heading=120)
sim.add_maneuver(time=108, speed=15, speed_unit='knots')
sim.add_maneuver(time=115, speed=20, speed_unit='knots')
sim.add_maneuver(time=120, speed=30, speed_unit='knots')
sim.add_turn_maneuver(turn_time=150, turn_rate=3, turn_speed=15, turn_speed_unit='knots', heading=135)


# Run simulation for 10 seconds
trajectory = sim.simulate(end_time=200)

for t, lat, lon in trajectory:
    print(f"t={t:.0f}s -> lat={lat:.6f}, lon={lon:.6f}")

# Use GeoDistance to find distance from start and end points of simulation.
geo = GeoDistance()

start_pos = (trajectory[0][1], trajectory[0][2])
end_pos = (trajectory[-1][1], trajectory[-1][2])

print(f"Distance (nmi): {geo.haversine_points(start_pos, end_pos):.2f} nmi")

# Plot simulated track
sim.track_plot(trajectory)