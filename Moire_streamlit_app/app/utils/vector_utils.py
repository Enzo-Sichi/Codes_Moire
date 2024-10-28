import streamlit as st
import plotly.graph_objects as go
import numpy as np
from typing import List, Tuple, Dict
from itertools import product

def calculate_fourier_coefficient(harmonic: int, thickness: float) -> float:
    """
    Calculate the Fourier coefficient magnitude for a given harmonic and pattern type.
    
    Args:
        harmonic: The harmonic number
        thickness: The thickness parameter (between 0 and 1)
        pattern_type: 'grid' or 'dot'
    
    Returns:
        float: The magnitude of the Fourier coefficient
    """
    tau_T = 1-thickness
    if harmonic == 0:
        return tau_T  # DC component
    
    # For non-zero harmonics
    return np.abs((1.0 / (np.pi * harmonic)) * np.sin(harmonic * np.pi * tau_T))

def calculate_fourier_coefficient(harmonic: int, thickness: float, inverted: bool = False) -> float:
    """
    Calculate the Fourier coefficient magnitude for a given harmonic and pattern type.
    
    Args:
        harmonic: The harmonic number
        thickness: The thickness parameter (between 0 and 1)
        inverted: Whether to calculate coefficients for inverted pattern
    
    Returns:
        float: The magnitude of the Fourier coefficient
    """
    tau_T = 1-thickness
    
    if inverted:
        # For inverted patterns, we need to flip the DC component and negate other harmonics
        if harmonic == 0:
            return 1 - tau_T  # Inverted DC component
        else:
            # For non-zero harmonics, phase is shifted by π
            return -np.abs((1.0 / (np.pi * harmonic)) * np.sin(harmonic * np.pi * tau_T))
    else:
        # Original coefficient calculation
        if harmonic == 0:
            return tau_T
        return np.abs((1.0 / (np.pi * harmonic)) * np.sin(harmonic * np.pi * tau_T))

def create_frequency_vectors(pattern_type: str, frequencies: List[float], 
                           angles: List[float], thicknesses: List[float]) -> List[Dict]:
    """
    Create base frequency vectors with proper Fourier coefficients.
    """
    vectors = []
    is_inverted = 'Inverted' in pattern_type
    
    for i, (f, theta, thickness) in enumerate(zip(frequencies, angles, thicknesses)):
        x = f * np.cos(np.radians(theta))
        y = f * np.sin(np.radians(theta))
        base_vector = np.array([x, y])
        
        if 'Dot' in pattern_type:
            perp_vector = np.array([-y, x])
            base_intensity = calculate_fourier_coefficient(1, thickness, is_inverted)
            
            vectors.append({
                'vector': base_vector,
                'index': i,
                'intensity': base_intensity,
                'pattern_type': pattern_type,
                'direction': 'horizontal',
                'base_vector': True,
                'thickness': thickness,
                'inverted': is_inverted
            })
            vectors.append({
                'vector': perp_vector,
                'index': i,
                'intensity': base_intensity,
                'pattern_type': pattern_type,
                'direction': 'vertical',
                'base_vector': True,
                'thickness': thickness,
                'inverted': is_inverted
            })
        else:
            base_intensity = calculate_fourier_coefficient(1, thickness, is_inverted)
            vectors.append({
                'vector': base_vector,
                'index': i,
                'intensity': base_intensity,
                'pattern_type': pattern_type,
                'direction': None,
                'base_vector': True,
                'thickness': thickness,
                'inverted': is_inverted
            })
    return vectors

def zero_harmonic_Intensity(base_vectors: List[Dict]) -> float:
    zero_harmonic_I = 1.0
    for base_vector in base_vectors:
        zero_harmonic_I *= calculate_fourier_coefficient(0, base_vector['thickness'], 
                                                       base_vector.get('inverted', False))
    return zero_harmonic_I

def create_all_vectors(base_vectors: List[Dict], nHarmonics: int,
                       intensity_ratio_threshold: float) -> List[Dict]:
    """
    Create all harmonic vector combinations with correct Fourier coefficients.
    """
    all_vectors = []
    direction_number = len(base_vectors)
    
    # Generate all possible combinations of harmonics
    harmonic_range = range(-nHarmonics, nHarmonics + 1)
    harmonic_combinations = product(harmonic_range, repeat=direction_number)
    
    zero_harmonic_I = zero_harmonic_Intensity(base_vectors)

    for combination in harmonic_combinations:
        vector = {
            'vector': np.array([0.0, 0.0]),
            'coordinates': [],
            'intensity': 1.0,
            'pattern_type': "",
            'direction': None,
            'base_vector': False
        }
        add_vector = True
        # Calculate combined vector and intensity
        for harmonic, base_vector in zip(combination, base_vectors):
            coef = calculate_fourier_coefficient(harmonic, base_vector['thickness'])
            vector['intensity'] *= coef
        
            if vector['intensity'] < intensity_ratio_threshold * zero_harmonic_I:
                add_vector = False
                break
            # Add to position vector
            vector['vector'] += harmonic * base_vector['vector']
            vector['coordinates'].append(harmonic)

            vector['pattern_type'] = base_vector['pattern_type']
        
        # Check if this is a base vector (only one non-zero harmonic)
        if vector['coordinates'].count(0) == direction_number - 1:
            vector['base_vector'] = True
        if add_vector:    
            all_vectors.append(vector)
    
    return all_vectors

def is_within_visibility_disk(vector: np.ndarray, disk_radius: float) -> bool:
    return np.linalg.norm(vector) <= disk_radius