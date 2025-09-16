#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 13 22:44:27 2025

@author: kpetchsaiprasert
"""

import math

class Quaternion:
    def __init__(self, w, x, y, z):
        self.w = w
        self.x = x
        self.y = y
        self.z = z
        
    def __repr__(self):
        return f"Quaternion({self.w:.4f}, {self.x:.4f}, {self.y:.4f}, {self.z:.4f})"
    
    def __mul__(self, other):
        """Hamiliton product"""
        w1, x1, y1, z1 = self.w, self.x, self.y, self.z
        w2, x2, y2, z2 = other.w, other.x, other.y, other.z 
        
        return Quaternion(
            w1*w2 - x1*x2 - y1*y2 - z1*z2,
            w1*x2 + x1*w2 + y1*z2 - z1*y2,
            w1*y2 - x1*z2 + y1*w2 + z1*x2,
            w1*z2 + x1*y2 - y1*x2 + z1*w2
        )
    
    def conjugate(self):
        return Quaternion(self.w, -self.x, -self.y, -self.z)
    
    def norm(self):
        return math.sqrt(self.w**2 + self.x**2 + self.y**2 + self.z**2)
    
    def normalize(self):
        n = self.norm()
        if n == 0:
            raise ZeroDivisionError("Cannot normalize a zero quaternion")
        self.w /= n
        self.x /= n
        self.y /= n
        self.z /= n
        return self
    
    def inverse(self):
        conj = self.conjugate()
        n2 = self.norm()**2
        return Quaternion(conj.w/n2, conj.x/n2, conj.y/n2, conj.z/n2)
    
    def to_rotation_matrix(self):
        w, x, y, z = self.w, self.x, self.y, self.z
        return [
            [1 - 2*(y**2 + z**2), 2*(x*y - z*w),         2*(x*z + y*w)],
            [2*(x*y + z*w),       1 - 2*(x**2 + z**2),   2*(y*z - x*w)],
            [2*(x*z - y*w),       2*(y*z + x*w),         1 - 2*(x**2 + y**2)]
        ]
    
    def rotate_vector(self, v):
        if len(v) != 3:
            raise ValueError("Vector must be 3-dimensional")
        q_vec = Quaternion(0, *v)
        q_rot = self * q_vec * self.inverse()
        return (q_rot.x, q_rot.y, q_rot.z)
    
    
    #----------------------------
    # Factory methods
    #----------------------------
    @classmethod 
    def from_axis_angle(cls, axis, angle_rad):
        """Create a quaternion from a rotation axis and angle (in radionas)"""
        if len(axis) != 3:
            raise ValueError("Axis must be a 3-element vector")
        x, y, z = axis
        norm = math.sqrt(x**2 + y**2 + z**2)
        if norm == 0:
            raise ValueError("Rotation axis cannot be zero vector")
        x /= norm
        y /= norm
        z /= norm
        half_angle = angle_rad / 2
        w = math.cos(half_angle)
        sin_half = math.sin(half_angle)
        return cls(w, x*sin_half, y*sin_half, z*sin_half)
    
    @classmethod
    def from_euler(cls, roll, pitch, yaw):
        """Create a quaternion form Euler angles (roll, pitch, yaw) in radions."""
        cy = math.cos(yaw * 0.5)
        sy = math.sin(yaw * 0.5)
        cp = math.cos(pitch * 0.5)
        sp = math.sin(pitch * 0.5)
        cr = math.cos(roll * 0.5)
        sr = math.sin(roll * 0.5)
        
        w = cr * cp * cy + sr * sp * sy
        x = sr * cp * cy - cr * sp * sy
        y = cr * sp * cy + sr * cp * sy
        z = cr * cp * sy - sr * sp * cy
        
        return cls(w, x, y, z).normalize()

#------------------------------------------------------
# Example usage
#------------------------------------------------------
if __name__ == "__main__":   
    # From axis-angle
    axis = (0, 0, 1) # rotate about z-axis
    angle = math.radians(90)
    q1 = Quaternion.from_axis_angle(axis, angle)
    print("Quaternion from axis-angle:", q1)

    # From Euler angles (roll, pitch, yaw)
    roll = math.radians(0)
    pitch = math.radians(0)
    yaw = math.radians(90)
    q2 = Quaternion.from_euler(roll, pitch, yaw)
    print("Quaternion from Euler angles:", q2)
    
    # Rotate a vector using the quaternion
    v = (1, 0, 0)
    v_rot = q1.rotate_vector(v)
    print("Rotated vector:", v_rot)