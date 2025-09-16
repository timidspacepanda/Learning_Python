#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 13 17:30:01 2025

@author: kpetchsaiprasert
"""

import numpy as np

class ECEFConverter:
    """
    Convert coordinates from ECEF to NED or ENU frames.
    
    Args:
        lat (float): Reference latitude in degrees
        lon (float): Reference longitude in degrees
        alt (flaot): Reference altitude in meters (optional, used for precision)
    """
    
    def __init__(self, lat: float, lon: float, alt: float =0):
        self.lat = np.deg2rad(lat)
        self.lon = np.deg2rad(lon)
        self.alt = alt # in meters
        
        # WGS84 ellipsoid constants
        self.a = 6378137.0 # semi-major axis (m)
        self.f = 1 / 298.257223563 # flattening
        self.e2 = self.f * (2 - self.f) # eccentricity^2
        
        # Precompute rotation matrices
        self.R_ecef_to_enu = np.array([
            [-np.sin(self.lon),                   np.cos(self.lon),                  0],
            [-np.sin(self.lat)*np.cos(self.lon), -np.sin(self.lat)*np.sin(self.lon), np.cos(self.lat)],
            [np.cos(self.lat)*np.cos(self.lon),   np.cos(self.lat)*np.sin(self.lon), np.sin(self.lat)] 
        ])
        
        # NED is just ENU with a reorder and flip
        self.R_ecef_to_ned = np.array([
            [-np.sin(self.lat)*np.cos(self.lon), -np.sin(self.lat)*np.sin(self.lon),  np.cos(self.lat)],
            [-np.sin(self.lon),                   np.cos(self.lon),                   0],
            [-np.cos(self.lat)*np.cos(self.lon), -np.cos(self.lat)*np.sin(self.lon), -np.sin(self.lat)]
        ])
        
        # Precompute observer ECEF position
        self.obs_ecef = self._lla_to_ecef(self.lat, self.lon, self.alt)
        
        
    def _lla_to_ecef(self, lat, lon, h):
        """ 
        Convert geodetic lat/lon to ECEF.
        """
        
        N = self.a / np.sqrt(1 - self.e2 * np.sin(lat)**2)
        x = (N + h) * np.cos(lat) * np.cos(lon)
        y = (N + h) * np.cos(lat) * np.sin(lon)
        z = (N * (1 - self.e2) + h) * np.sin(lat)
        return np.array([x, y, z])
        
    def ecef_to_enu(self, ecef_vector):
        """
        Convert a vector from ECEF to ENU frame.

        """
        return self.R_ecef_to_enu @ ecef_vector
    
    def ecef_to_ned(self, ecef_vector):
        """
        Convert a vector from ECEF to NED frame.
        """
        
        return self.R_ecef_to_ned @ ecef_vector
    
    def ned_to_enu(self, ned_vector):
        """
        Convert to vector from NED to ENU frame.
        """
        
        # NED to ENU = swap N<->E, invert Down to Up
        N, E, D = ned_vector
        return np.array([E, N, -D])
    
    def enu_to_ned(self, enu_vector):
        """
        Convert a vector from ENU to NED frame.
        """
        
        E, N, U = enu_vector
        return np.array([N, E, -U])
    
    def ecef_to_horizon(self, target_ecef):
        """ Convert ECEF target to local horizon (az, el, range). """
        # Relative vector
        rel_vec = target_ecef - self.obs_ecef
        
        # Rotate into ENU
        enu = self.ecef_to_enu(rel_vec)
        
        e, n, u = enu
        
        # Convert ENU to Azimuth, Elevation, Range
        rng = np.linalg.norm(enu)
        az =  np.degrees(np.arctan2(e, n)) % 360.0
        el = np.degrees(np.arctan2(u, np.sqrt(e**2 + n**2)))
        
        return az, el, rng
    
    def _rotation_matrix_body(self, yaw, pitch, roll):
        """Rotation matrix from NED -> Body (radians)."""
        
        cy, sy = np.cos(yaw), np.sin(yaw)
        cp, sp = np.cos(pitch), np.sin(pitch)
        cr, sr = np.cos(roll), np.sin(roll)
        
        Rz = np.array([[ cy, sy, 0],
                       [-sy, cy, 0], 
                       [  0,  0, 1]])
        
        Ry = np.array([[ cp, 0, -sp],
                       [  0, 1,   0],
                       [ sp, 0,  cp]])
        
        Rx = np.array([[1, 0, 0],
                       [0, cr, sr],
                       [0, -sr, cr]])
        
        return Rx @ Ry @ Rz
        
    def ecef_to_body(self, target_ecef, yaw_deg, pitch_deg, roll_deg):
        """Convert ECEF target vector to Body frame coordinates"""
        # Relative vector
        rel_vec = target_ecef - self.obs_ecef
        
        # Step 1: ECEF to NED
        ned = self.ecef_to_ned(rel_vec)
        
        # Step 2: NED to Body
        yaw, pitch, roll = map(np.radians, (yaw_deg, pitch_deg, roll_deg))
        R_body = self._rotation_matrix_body(yaw, pitch, roll)
        body_vec = R_body @ ned
        
        return body_vec
    
#------------------------------------------------------
# Example usage
#------------------------------------------------------
if __name__ == "__main__":
    converter = ECEFConverter(lat=37.7749, lon=122.4194)
    
    # Example ECEF vector (x, y, z) in meters
    ecef_vec = np.array([1000, 2000, 3000])
    
    enu_vec = converter.ecef_to_enu(ecef_vec)
    ned_vec = converter.ecef_to_ned(ecef_vec)
    
    print("ECEF:", ecef_vec)
    print("ENU :", enu_vec)
    print("NED :", ned_vec)
    
    # Convert NED to ENU
    enu_from_ned = converter.ned_to_enu(ned_vec)
    print("ENU from NED:", enu_from_ned)
    
    # Observer: (lat, lon, alt) = (40N, 105W, 1600 m)
    new_converter = ECEFConverter(40.0, -105.0, 1600)
    
    # Target: arbitrary ECEF point
    target_ecef = np.array([1.1e6, -4.8e6, 4.0e6])
    
    az, el, rng = new_converter.ecef_to_horizon(target_ecef)
    print(f"Azimuth: {az:.2f}deg, Elevation: {el:.2f}deg, Range: {rng/1000:.2f} km")
    
    # Aircraft orientation (yaw=90deg, pitch=5deg, roll=2deg)
    body_coords = new_converter.ecef_to_body(target_ecef, 90, 5, 2)
    print("Target in Body frame:", body_coords)