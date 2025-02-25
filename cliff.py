import numpy as np
import matplotlib.pyplot as plt
from math import radians, sin, cos

# Constants
EARTH_RADIUS = 6371000  # Earth's radius in meters

# Simulate user data
def generate_user_data(n=50):
    """Generate fake user data: lat, lon, distance, and azimuth"""
    users = []


# Calculate cliff coordinates based on user position, distance to cliff, and azimuth
def calculate_cliff(lat, lon, distance, azimuth):
    """ Calculate the cliff's coordinates based on user's position, distance to cliff, and azimuth. Assumes azimuth is north (0 degrees), so only longitude will change. """
    # rads
    lat_rad = radians(lat)
    lon_rad = radians(lon)
    
    # lon lat
    dlat = distance / EARTH_RADIUS * cos(radians(azimuth))
    dlon = distance / EARTH_RADIUS * sin(radians(azimuth)) / cos(lat_rad)
    
    # degrees
    new_lat = lat + (dlat * 180 / np.pi)
    new_lon = lon + (dlon * 180 / np.pi)
    
    return new_lat, new_lon

# cliff and ocean, should probs move ocean to a different function
def plot_cliff(users):
    cliff_points = []
    previous_cliff_2024_points = []
    previous_cliff_2023_points = []
    previous_cliff_2026_points = []
    prev_cliff_lon = None  # Track the previous cliff longitude to avoid crossing, CAN STILL SPAWN IN FUCKED WAYS, icba its rare enough
    
    # lowest user, plots ocean
    min_user_lat = min(user[0] for user in users)  
    ocean_latitude = min_user_lat - 0.05  # ocean always spawns in 0.05 below lowest user
    
    # ocean line, truly groundbreaking 
    plt.axhline(ocean_latitude, color='blue', linestyle='--', label="Ocean Line")
    
    # Calculate each user's cliff point and draw a dotted line
    for user in users:
        lat, lon, distance, azimuth = user
        cliff_lat, cliff_lon = calculate_cliff(lat, lon, distance, azimuth)
        
        # Ensure the cliff does not cross itself (must move in a consistent direction)
        if prev_cliff_lon is not None and cliff_lon < prev_cliff_lon:  # If the cliff would move backwards (crossing over itself), skip this user data
            continue
        
        # to prevent too much criss cross apple sauce
        prev_cliff_lon = cliff_lon
        
        # user location
        plt.scatter(lon, lat, color='blue')
        
        # Plot the cliff location
        cliff_points.append((cliff_lat, cliff_lon))
        plt.scatter(cliff_lon, cliff_lat, color='red', marker='x')
        
        # Calculate the previous cliff (2024)
        previous_cliff_2024_lat = cliff_lat - np.random.uniform(20, 80) * 0.0001  # lowering lat
        previous_cliff_2024_points.append((previous_cliff_2024_lat, cliff_lon))
        
        # Calculate the previous cliff (2023)
        previous_cliff_2023_lat = previous_cliff_2024_lat - np.random.uniform(20, 80) * 0.0001  # Shift lat more
        previous_cliff_2023_points.append((previous_cliff_2023_lat, cliff_lon))
        
        # Calculate the 2026 cliff (current cliff)
        previous_cliff_2026_lat = cliff_lat + np.random.uniform(20, 80) * 0.0001  # Shift lat up
        previous_cliff_2026_points.append((previous_cliff_2026_lat, cliff_lon))
        
        # Plot previous cliff location (2024)
        plt.scatter(cliff_lon, previous_cliff_2024_lat, color='orange', marker='x')
        
        # Plot previous cliff location (2023)
        plt.scatter(cliff_lon, previous_cliff_2023_lat, color='purple', marker='x')
        
        # Plot previous cliff location (2026)
        plt.scatter(cliff_lon, previous_cliff_2026_lat, color='cyan', marker='x')
        
        # Plot dotted line from user to cliff
        plt.plot([lon, cliff_lon], [lat, cliff_lat], linestyle=':', color='green', alpha=0.5)
    
    # Plot the final connected cliff line (original)
    cliff_points = np.array(cliff_points)
    plt.plot(cliff_points[:, 1], cliff_points[:, 0], color='black', label="Cliff Edge (Current)", linewidth=2)
    
    # Plot the 2024 cliff line
    previous_cliff_2024_points = np.array(previous_cliff_2024_points)
    plt.plot(previous_cliff_2024_points[:, 1], previous_cliff_2024_points[:, 0], color='orange', label="2024 Cliff Edge", linestyle='--', linewidth=2)
    
    # Plot the 2023 cliff line
    previous_cliff_2023_points = np.array(previous_cliff_2023_points)
    plt.plot(previous_cliff_2023_points[:, 1], previous_cliff_2023_points[:, 0], color='purple', label="2023 Cliff Edge", linestyle='-.', linewidth=2)
    
    # Plot the 2026 cliff line
    previous_cliff_2026_points = np.array(previous_cliff_2026_points)
    plt.plot(previous_cliff_2026_points[:, 1], previous_cliff_2026_points[:, 0], color='cyan', label="2026 Cliff Edge", linestyle=':', linewidth=2)
    
    # Plot settings
    plt.title("Mapped Cliff Points with User Data (Current, 2024, 2023, and 2026)")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.grid(True)
    plt.legend()
    plt.show()
    
# Generate fake data with more users and further distances
users = generate_user_data(50)  # Simulate 50 users
#img = plt.imread("cliff.png")
#fig, ax = plt.subplots()
#ax.imshow(img)
# Plot the cliffs
plot_cliff(users)
