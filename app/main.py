import streamlit as st
from utils.visualization_handlers import (
    create_pattern_figure,
    create_spectrum_figure,
    create_frequency_vector_figure
)
from utils.input_controls import get_input_controls
from utils.pattern_utils import create_pattern
from utils.vector_utils import create_frequency_vectors, create_all_vectors
from utils.fourier_utils import compute_fourier_transform, compute_inverse_fourier
import numpy as np

def main():
    st.set_page_config(layout="wide", menu_items={'Get help': None, 'Report a bug': None, 'About': None})
    
    # Make the layout more compact by using custom CSS
    st.markdown("""
        <style>
        .stSlider {
            padding-bottom: 2px;
        }
        .block-container {
            padding-top: 1rem;
            padding-bottom: 0rem;
        }
        h1, h2, h3, h4, h5, h6 {
            margin: 0px;
            padding: 0px;
        }
        .row-widget {
            min-height: 0px;
            padding: 0px;
        }
        .stRadio > label {
            margin-bottom: 0px;
        }
        </style>
    """, unsafe_allow_html=True)

    (pattern_types, frequencies, angles, thicknesses, circle_positions, 
     visibility_radius, window_half_size, view_mode, 
     intensity_threshold, n_harmonics) = get_input_controls()

    # Generate pattern and computations
    pattern_size = 700
    combined_pattern = np.ones((pattern_size, pattern_size))
    
    # Create individual patterns and combine them
    for pattern_type, freq, angle, thickness, circle_position in zip(
        pattern_types, frequencies, angles, thicknesses, circle_positions):
        combined_pattern *= create_pattern(
            pattern_size, freq, angle, thickness, pattern_type, circle_position)
    
    fourier_spectrum,abs_fourier_spectrum = compute_fourier_transform(combined_pattern, window_half_size,visibility_radius)
    inverse_fourier = compute_inverse_fourier(fourier_spectrum)
    
     
    base_vectors = create_frequency_vectors(pattern_type, frequencies, angles,thicknesses)
    all_vectors = create_all_vectors(base_vectors, n_harmonics,intensity_threshold)
    
    # Display visualizations based on selected mode
    left_col, right_col = st.columns(2)
    
    if view_mode == "Pattern & Frequency":
        with left_col:
            st.markdown("##### Pattern")
            pattern_fig = create_pattern_figure(combined_pattern)
            st.plotly_chart(pattern_fig, use_container_width=True, config={'displayModeBar': True, 'scrollZoom': True})
            
        with right_col:
            st.markdown("##### Frequency Domain")
            freq_fig = create_frequency_vector_figure(all_vectors, base_vectors, visibility_radius, window_half_size)
            st.plotly_chart(freq_fig, use_container_width=True)
    else:  # Fourier Analysis mode
        with left_col:
            st.markdown("##### Inverse Fourier Transform")
            inverse_fig = create_pattern_figure(inverse_fourier)
            st.plotly_chart(inverse_fig, use_container_width=True)
            
        with right_col:
            st.markdown("##### Fourier Transform")
            fourier_fig = create_spectrum_figure(abs_fourier_spectrum, window_half_size,visibility_radius)
            st.plotly_chart(fourier_fig, use_container_width=True)

    st.write("")  # Add some space
    st.write("")

    # Explanation section below the visualizations
    with st.expander("How to Use This App", icon="🚨"):
        st.markdown("""
        This application helps visualize and analyze grid patterns and their frequency components. Here's how to use it:

        #### Biggest Tip
        - **The Moire effect is based on the creation of low frequency components** 
        - **In the frequency domain, try to put the red dots as close as possible to the center with far away blue dots**
        - That will mean that with thin patterns (high frequency) you can produce big visual effects (low frequency)            

        #### Controls
        - **Pattern Type**: Choose between different types of grid patterns
        - **View Mode**: Switch between two visualization modes:
            - Pattern & Frequency: Shows the actual pattern and its frequency domain representation
            - Fourier Analysis: Shows the Fourier transform and its inverse
        - **Grid Controls**: For each grid component:
            - Frequency: Adjust the spacing of the grid lines
            - Angle: Control the rotation of the grid
        - **Visibility Radius**: Adjust the size of the visible frequency domain
        - **Window Range**: Control the display range of the frequency domain plot

        #### Visualization Modes
        1. **Pattern & Frequency Mode**
            - Left: Shows the actual grid pattern
            - Right: Displays the frequency domain representation with vectors
        
        2. **Fourier Analysis Mode**
            - Left: Shows the inverse Fourier transform
            - Right: Displays the Fourier transform magnitude spectrum

        #### Tips
        - Try adjusting frequencies and angles to see how they affect the pattern
        - Compare the frequency domain representation with the Fourier transform
        - Experiment with different pattern types to understand their frequency components

        ## Biggest Tip
        The Moire effect is based on the creation of low frequency components. 
        in the frequency domain, try to put the red dots as close as possible to the center with far away blue dots. 
        That will mean that with thin patterns (high frequency) you can produce big visual effects (low frequency).
                

        """)

if __name__ == "__main__":
    main()