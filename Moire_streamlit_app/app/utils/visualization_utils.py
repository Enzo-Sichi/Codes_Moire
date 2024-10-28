import streamlit as st
import plotly.graph_objects as go
import numpy as np
from typing import List, Tuple, Dict
from itertools import product
from utils.vector_utils import *

def frequency_domain_visualization(all_vectors,visibility_radius): 
    x_coords = []
    y_coords = []
    labels = []
    intensities = []
    for vector in all_vectors:
        if not(is_within_visibility_disk(vector['vector'], visibility_radius)):
            continue
        x_coords.append(vector['vector'][0])
        y_coords.append(vector['vector'][1])
        labels.append(str(tuple(vector['coordinates'])))
        intensities.append(vector['intensity'])

        colors = ['rgba(255, 0, 0, {:.2f})'.format(intensity) for intensity in intensities]

        freq_fig = go.Figure()
        freq_fig.add_trace(go.Scatter(
            x=x_coords,
            y=y_coords,
            mode='markers+text',
            name='Vector Sums',
            marker=dict(color=colors, size=6, symbol='circle'),
            text=labels,
            textposition="top center"
        ))

    # Visibility disk
    theta = np.linspace(0, 2*np.pi, 100)
    x_circle = visibility_radius * np.cos(theta)
    y_circle = visibility_radius * np.sin(theta)
    freq_fig.add_trace(go.Scatter(
        x=x_circle, y=y_circle,
        mode='lines',
        name='Visibility Disk',
        line=dict(dash='dash', color='gray')
    ))
        
    # colors = ['blue', 'green', 'red', 'purple']
    # freq_fig.add_trace(go.Scatter(
    # x=[0, harmonic_vector[0]], 
    # y=[0, harmonic_vector[1]],
    # mode='lines',
    # # name=name,
    # line=dict(color=color, width=2),
    # marker=dict(size=8)
    # ))

    return(freq_fig)