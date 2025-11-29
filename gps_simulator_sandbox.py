from gps_simulator import GPS_Simulator

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
sim.add_maneuver(time=45, speed=2, heading=55)
sim.add_maneuver(time=60, speed=30, speed_unit='knots', heading=60)

# Run simulation for 10 seconds
trajectory = sim.simulate(end_time=120)

for t, lat, lon in trajectory:
    print(f"t={t:.0f}s -> lat={lat:.6f}, lon={lon:.6f}")

sim.track_plot(trajectory)