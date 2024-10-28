import numpy as np
import plotly.graph_objects as go
import streamlit as st
from utils.vector_utils import create_frequency_vectors, create_all_vectors, is_within_visibility_disk,zero_harmonic_Intensity
from utils.pattern_utils import create_pattern
from utils.fourier_utils import compute_fourier_transform, compute_inverse_fourier

def create_pattern_figure(pattern):
    fig = go.Figure(data=go.Heatmap(
        z=1 - pattern,  
        colorscale='Greys',
        showscale=False  # Hide colorbar
    ))
    fig.update_layout(
        width=700,  # Increased size
        height=700,  # Increased size
        xaxis=dict(showticklabels=False, showgrid=False, scaleanchor="y", scaleratio=1),
        yaxis=dict(showticklabels=False, showgrid=False),
        margin=dict(l=0, r=0, t=25, b=0),  # Minimal margins, small top margin for title
        paper_bgcolor='rgba(0,0,0,0)',  # Transparent background
        plot_bgcolor='rgba(0,0,0,0)'
    )
    return fig

def create_spectrum_figure(spectrum, window_half_size,visibility_radius):
    # Create frequency axes
    N = spectrum.shape[0]
    freq_step = (2 * window_half_size) / N
    frequencies = np.arange(-window_half_size, window_half_size, freq_step)
    
    magnitude_spectrum = np.abs(spectrum)
    magnitude_spectrum = np.log1p(magnitude_spectrum)
    magnitude_spectrum = (magnitude_spectrum - np.min(magnitude_spectrum)) / (
        np.max(magnitude_spectrum) - np.min(magnitude_spectrum))
    


    fig = go.Figure(data=go.Heatmap(
        z=magnitude_spectrum,
        x=frequencies,
        y=frequencies,
        colorscale='Viridis',
        showscale=False
    ))
    
            # Add visibility disk
    if visibility_radius < 0.85*window_half_size:
        theta = np.linspace(0, 2*np.pi, 100)
        x_circle = visibility_radius * np.cos(theta)
        y_circle = visibility_radius * np.sin(theta)
        fig.add_trace(go.Scatter(
            x=x_circle, y=y_circle,
            mode='lines',
            name='Visibility Disk',
            line=dict(dash='dash', color='red')
        ))
    # else:
    #         fig.add_annotation(
    #     x=0,  # You can customize where the text appears
    #     y=-window_half_size+10,
    #     text="Visibility radius is too large for the current window size.",
    #     showarrow=False,
    #     font=dict(size=14, color="red")
    # )

    fig.update_layout(
        width=700,
        height=700,
        xaxis=dict(
            title='fx',
            showgrid=True,
            scaleanchor="y", 
            scaleratio=1,
            gridcolor='rgba(128, 128, 128, 0.2)',
            zeroline=True,
            zerolinewidth=2,
            zerolinecolor='rgba(128, 128, 128, 0.5)'
        ),
        yaxis=dict(
            title='fy',
            showgrid=True,
            gridcolor='rgba(128, 128, 128, 0.2)',
            zeroline=True,
            zerolinewidth=2,
            zerolinecolor='rgba(128, 128, 128, 0.5)'
        ),
        margin=dict(l=50, r=0, t=25, b=50),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    return fig

def get_pattern_color(index, pattern_type):
    # Define a color palette
    colors = ['rgb(31, 119, 180)', 'rgb(255, 127, 14)', 
             'rgb(44, 160, 44)', 'rgb(214, 0, 200)', 
             'rgb(148, 103, 189)', 'rgb(140, 86, 75)', 
             'rgb(230, 190, 147)']

    return colors[index]

def create_frequency_vector_figure(all_vectors, base_vectors, visibility_radius, window_half_size):
    freq_fig = go.Figure()
    
    # First, draw harmonic lines of the base vectors.
    for vector in base_vectors:
        
        angle = np.arctan2(vector['vector'][1], vector['vector'][0])
        length = window_half_size * 2  # Make lines span the entire window
        
        x1 = -length * np.cos(angle)
        y1 = -length * np.sin(angle)
        x2 = length * np.cos(angle)
        y2 = length * np.sin(angle)
        
        color = get_pattern_color(vector['index'], vector['pattern_type'])

        # Add the line
        freq_fig.add_trace(go.Scatter(
            x=[x1, x2],
            y=[y1, y2],
            mode='lines',
            line=dict(color=color, width=3),  # Very thin lines
            opacity=1,  
            hoverinfo='skip'
        ))
    
    # Then add vector points
    x_coords = []
    y_coords = []
    labels = []
    hover_texts = []
    colors = []
    zero_harmonic_I = zero_harmonic_Intensity(base_vectors)

    for vector in all_vectors:
        if (not (is_within_visibility_disk(vector['vector'], visibility_radius)) and  vector['base_vector'] == False):
            continue

        x_coords.append(vector['vector'][0])
        y_coords.append(vector['vector'][1])
        labels.append(str(tuple(vector['coordinates'])))  # Only coordinates for text display
        hover_texts.append(f"Intensity: {vector['intensity']/zero_harmonic_I:.2f}")  # Intensity for hover
        
        # Create red color with intensity-based opacity
        if vector['base_vector']:
            color = f'rgba(0, 0, 0, {vector["intensity"]/zero_harmonic_I+0.001})'
        else:
            color = f'rgba(255, 0, 0, {vector["intensity"]/zero_harmonic_I+0.001})'
        colors.append(color)

    # Add vector points
    freq_fig.add_trace(go.Scatter(
        x=x_coords,
        y=y_coords,
        mode='markers+text',
        name='Vector Sums',
        marker=dict(color=colors, size=8, symbol='circle'),
        text=labels,
        hovertext=hover_texts,
        textposition="top center"
    ))

    # Add visibility disk
    theta = np.linspace(0, 2*np.pi, 100)
    x_circle = visibility_radius * np.cos(theta)
    y_circle = visibility_radius * np.sin(theta)
    freq_fig.add_trace(go.Scatter(
        x=x_circle, y=y_circle,
        mode='lines',
        name='Visibility Disk',
        line=dict(dash='dash', color='red')
    ))

    freq_fig.update_layout(
        width=700,
        height=700,
        xaxis=dict(
            title='fx',
            range=[-window_half_size, window_half_size],
            zeroline=True,
            zerolinewidth=1,
            zerolinecolor='black',
            scaleanchor="y",
            scaleratio=1,
            showgrid=True,
            gridcolor='rgba(128, 128, 128, 0.2)'
        ),
        yaxis=dict(
            title='fy',
            range=[-window_half_size, window_half_size],
            zeroline=True,
            zerolinewidth=1,
            zerolinecolor='black',
            showgrid=True,
            gridcolor='rgba(128, 128, 128, 0.2)'
        ),
        showlegend=False,
        margin=dict(l=50, r=0, t=25, b=50),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    return freq_fig