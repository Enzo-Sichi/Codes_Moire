import streamlit as st
import math

def initialize_pattern_state():
    """Initialize the session state for pattern parameters if not already present."""
    if 'pattern_params' not in st.session_state:
        st.session_state.pattern_params = {
            'frequencies': [40.0] * 4,  # Store up to 4 frequencies
            'angles': [i * (180 / 4) for i in range(4)],  # Store up to 4 angles
            'thicknesses': [0.5] * 4,  # Store up to 4 thicknesses
            'circle_positions': [(0, 0)] * 4,  # Store up to 4 circle positions
            'R_values': [0.0] * 4,  # Store R values for circle positions
            'theta_values': [0.0] * 4  # Store theta values for circle positions
        }

def get_input_controls():
    initialize_pattern_state()
    st.markdown("""
    <style>
    /* Make the slider handle (the draggable circle) bigger */
    .stSlider [data-baseweb="slider"] [data-testid="stThumbValue"] {
    width: 25px !important;
    height: 25px !important;
    margin-top: -11px !important;   
    }
    </style>
    """, unsafe_allow_html=True)
    
    # First row: Pattern type, view mode, and intensity threshold
    col1, col2, col3a, col3b = st.columns([1, 1.5, 1, 0.5])
    with col1:
        pattern_type = st.selectbox("Pattern Type", 
            ["2 Vertical Grids", "3 Vertical Grids", "4 Vertical Grids", "2 Concentric Circles",
            "2 Dot Grids", "3 Dot Grids", "2 Inverted Dot Grids (Intensity in frequency domain incorrect)", 
            "3 Inverted Dot Grids (Intensity in frequency domain incorrect)))"])
    with col2:
        view_mode = st.radio("View Mode", 
            ["Pattern & Frequency", "Fourier Analysis"], 
            horizontal=True)
    
    is_concentric = "Concentric" in pattern_type

    # Second row: All sliders in one row
    num_patterns = int(pattern_type[0])
    slider_cols = st.columns(num_patterns + 2)  # +2 for visibility and window controls
    
    # Initialize lists for parameters
    frequencies = []
    angles = []
    thicknesses = []
    circle_positions = []
    
    # Parameter controls for each pattern
    for i in range(num_patterns):
        with slider_cols[i]:
            st.write(f"{'Circle' if is_concentric else 'Grid'} {i+1}")
            
            if is_concentric:
                # Update frequency in session state
                freq = st.slider(
                    f"Frequency {i+1}", 
                    10.0, 100.0, 
                    st.session_state.pattern_params['frequencies'][i], 
                    0.1
                )
                st.session_state.pattern_params['frequencies'][i] = freq
                
                # Update thickness in session state
                thickness = st.slider(
                    f"Thickness {i+1}", 
                    0.1, 0.9, 
                    st.session_state.pattern_params['thicknesses'][i], 
                    0.1
                )
                st.session_state.pattern_params['thicknesses'][i] = thickness
                
                if i > 0:  # Only show position control for second circle
                    R = st.slider(
                        f"R {i+1}", 
                        0.0, 100.0, 
                        st.session_state.pattern_params['R_values'][i], 
                        1.0
                    )
                    theta = st.slider(
                        r"$\theta_{{{}}}$".format(i+1), 
                        -180.0, 180.0, 
                        st.session_state.pattern_params['theta_values'][i], 
                        1.0
                    )
                    
                    # Store R and theta values
                    st.session_state.pattern_params['R_values'][i] = R
                    st.session_state.pattern_params['theta_values'][i] = theta
                    
                    pos_x = R * math.cos(math.radians(theta))
                    pos_y = R * math.sin(math.radians(theta))
                    circle_positions.append((pos_x, pos_y))
                else:
                    circle_positions.append((0, 0))  # First circle always at center
                angles.append(0)  # Not used for circles but kept for compatibility
            else:
                # Update frequency in session state
                freq = st.slider(
                    f"Frequency {i+1}", 
                    10.0, 100.0, 
                    st.session_state.pattern_params['frequencies'][i], 
                    0.1
                )
                st.session_state.pattern_params['frequencies'][i] = freq
                
                # Update angle in session state
                angle = st.slider(
                    f"Angle {i+1}", 
                    0.0, 360.0, 
                    st.session_state.pattern_params['angles'][i], 
                    1.0
                )
                st.session_state.pattern_params['angles'][i] = angle
                
                # Update thickness in session state
                thickness = st.slider(
                    f"Thickness {i+1}", 
                    0.1, 0.9, 
                    st.session_state.pattern_params['thicknesses'][i], 
                    0.1
                )
                st.session_state.pattern_params['thicknesses'][i] = thickness
                
                angles.append(angle)
                circle_positions.append((0, 0))  # Not used for grids
            
            frequencies.append(freq)
            thicknesses.append(thickness)
    
    # Visibility and window controls
    with slider_cols[-2]:
        st.write("Visibility")
        n_harmonics = st.slider("Number of Harmonics (1 for complex patterns)", 1, 10, 4, 1)
        intensity_threshold = st.slider("Intensity Threshold (above 0.1 for complex patterns)", 0.0, 0.5, 0.05, 0.01)
    
    with slider_cols[-1]:
        st.write("Window")
        window_half_size = st.slider("Range", 5.0, 200.0, 100.0, 5.0)
        visibility_radius = st.slider("Radius", 1.0, 200.0, 100.0, 1.0)

    return (pattern_type, frequencies, angles, thicknesses, circle_positions, 
            visibility_radius, window_half_size, view_mode, intensity_threshold, n_harmonics)