import streamlit as st
import math

def initialize_state():
    """Initialize session state for all possible patterns"""
    if 'pattern_params' not in st.session_state:
        st.session_state.pattern_params = {
            'frequency': {i: 40.0 for i in range(10)},
            'angle': {i: i * 45.0 for i in range(10)},
            'thickness': {i: 0.5 for i in range(10)},
            'R': {i: 0.0 for i in range(10)},
            'theta': {i: 0.0 for i in range(10)}
        }

def handle_value_change(param_type, pattern_idx):
    """Callback function to handle slider value changes"""
    key = f"{param_type}_{pattern_idx}"
    if key in st.session_state:
        st.session_state.pattern_params[param_type][pattern_idx] = st.session_state[key]

def get_input_controls():
    initialize_state()
    
    # First row: Pattern selection, view mode
    col1, col2 = st.columns([2, 1])
    
    # Create pattern checkboxes
    with col1:
        st.write("Select Patterns")
        pattern_col1, pattern_col2, pattern_col3 = st.columns(3)
        
        active_patterns = []
        
        with pattern_col1:
            st.write("Regular Grids")
            if st.checkbox("Grid A", value=True):
                active_patterns.append(("Line Grid A", "Grid", 0))
            if st.checkbox("Grid B"):
                active_patterns.append(("Line Grid B", "Grid", 1))
            if st.checkbox("Grid C"):
                active_patterns.append(("Line Grid C", "Grid", 2))
            if st.checkbox("Grid D"):
                active_patterns.append(("Line Grid D", "Grid", 3))
        
        with pattern_col2:
            st.write("Circle Patterns")
            if st.checkbox("Circle A"):
                active_patterns.append(("Circle A", "Circle", 4))
            if st.checkbox("Circle B"):
                active_patterns.append(("Circle B", "Circle", 5))
        
        with pattern_col3:
            st.write("Dot Patterns")
            if st.checkbox("Dot Grid A"):
                active_patterns.append(("Dot Grid A", "Dot", 6))
            if st.checkbox("Dot Grid B"):
                active_patterns.append(("Dot Grid B", "Dot", 7))
            if st.checkbox("Inverted Dot A"):
                active_patterns.append(("Inverted Dot A", "InvertedDot", 8))
    
    with col2:
        view_mode = st.radio("View Mode", 
            ["Pattern & Frequency", "Fourier Analysis"], 
            horizontal=True)
    
    if not active_patterns:
        active_patterns = [("Grid A", "Grid", 0)]
    
    num_patterns = len(active_patterns)
    slider_cols = st.columns(num_patterns + 2)
    
    frequencies = []
    angles = []
    thicknesses = []
    circle_positions = []
    pattern_types = []
    
    for col_idx, (pattern_name, pattern_type, pattern_idx) in enumerate(active_patterns):
        with slider_cols[col_idx]:
            st.write(pattern_name)
            pattern_types.append(pattern_type)
            
            # Frequency slider
            freq_key = f"frequency_{pattern_idx}"
            freq = st.slider(
                "Frequency", 10.0, 100.0,
                value=st.session_state.pattern_params['frequency'][pattern_idx],
                key=freq_key,
                on_change=handle_value_change,
                args=('frequency', pattern_idx),
                step=0.1
            )
            frequencies.append(freq)
            
            # Thickness slider
            thick_key = f"thickness_{pattern_idx}"
            thickness = st.slider(
                "Thickness", 0.1, 0.9,
                value=st.session_state.pattern_params['thickness'][pattern_idx],
                key=thick_key,
                on_change=handle_value_change,
                args=('thickness', pattern_idx),
                step=0.1
            )
            thicknesses.append(thickness)
            
            if pattern_type == "Circle":
                angles.append(0)
                
                # R slider
                r_key = f"R_{pattern_idx}"
                R = st.slider(
                    "R", 0.0, 100.0,
                    value=st.session_state.pattern_params['R'][pattern_idx],
                    key=r_key,
                    on_change=handle_value_change,
                    args=('R', pattern_idx),
                    step=1.0
                )
                
                # Theta slider
                theta_key = f"theta_{pattern_idx}"
                theta = st.slider(
                    r"$\theta$", -180.0, 180.0,
                    value=st.session_state.pattern_params['theta'][pattern_idx],
                    key=theta_key,
                    on_change=handle_value_change,
                    args=('theta', pattern_idx),
                    step=1.0
                )
                
                pos_x = R * math.cos(math.radians(theta))
                pos_y = R * math.sin(math.radians(theta))
                circle_positions.append((pos_x, pos_y))
            else:
                # Angle slider
                angle_key = f"angle_{pattern_idx}"
                angle = st.slider(
                    "Angle", 0.0, 360.0,
                    value=st.session_state.pattern_params['angle'][pattern_idx],
                    key=angle_key,
                    on_change=handle_value_change,
                    args=('angle', pattern_idx),
                    step=1.0
                )
                angles.append(angle)
                circle_positions.append((0, 0))
    
    # Visibility and window controls (no persistence needed)
    with slider_cols[-2]:
        st.write("Visibility")
        n_harmonics = st.slider("Number of Harmonics", 1, 10, 4, 1)
        intensity_threshold = st.slider("Intensity Threshold", 0.0, 0.5, 0.05, 0.01)
    
    with slider_cols[-1]:
        st.write("Window")
        window_half_size = st.slider("Range", 5.0, 200.0, 100.0, 5.0)
        visibility_radius = st.slider("Radius", 1.0, 200.0, 100.0, 1.0)

    return (pattern_types, frequencies, angles, thicknesses, circle_positions, 
            visibility_radius, window_half_size, view_mode, intensity_threshold, n_harmonics)