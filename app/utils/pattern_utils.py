import numpy as np

def create_pattern(size: int, frequency: float, angle: float, thickness: float, 
                  pattern_type: str, circle_position: tuple = (0, 0)) -> np.ndarray:
    x = np.linspace(-size/2, size/2, size)
    y = np.linspace(-size/2, size/2, size)
    X, Y = np.meshgrid(x, y)
    
    if 'Concentric' in pattern_type:
        # Existing concentric circle logic...
        X_shifted = X - circle_position[0]
        Y_shifted = Y - circle_position[1]
        R = np.sqrt(X_shifted**2 + Y_shifted**2)
        period = size / frequency
        return (R % period) < (period * (1-thickness))
    else:
        theta = np.radians(angle)
        X_rot = X * np.cos(theta) + Y * np.sin(theta)
        Y_rot = -X * np.sin(theta) + Y * np.cos(theta)
        
        if 'Dot' in pattern_type:
            pattern = ((X_rot % (size/frequency) < (size/frequency) * (1-thickness)) & 
                      (Y_rot % (size/frequency) < (size/frequency) * (1-thickness)))
            return ~pattern if 'Inverted' in pattern_type else pattern
        else:
            return X_rot % (size/frequency) < (size/frequency) * (1-thickness)