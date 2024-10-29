import numpy as np
from scipy.fft import fft2, ifft2, fftshift, ifftshift

def apply_2d_hanning(pattern):
    """Apply a 2D Hanning window to the pattern."""
    rows, cols = pattern.shape
    hanning_1d_rows = np.hanning(rows)
    hanning_1d_cols = np.hanning(cols)
    hanning_2d = np.outer(hanning_1d_rows, hanning_1d_cols)
    return pattern * hanning_2d

def compute_fourier_transform(pattern: np.ndarray, window_half_size: float = 100.0 , visibility_radius: float = 50.0 ) -> np.ndarray:
    """
    Compute the 2D Fourier transform of the pattern.
    
    Args:
        pattern: Input pattern array
        window_half_size: Half size of the frequency window for proper scaling
    """
    # Apply Hanning window to reduce edge effects
    windowed_pattern = apply_2d_hanning(pattern)
    original_fourier = fftshift(fft2(pattern))
    # Apply FFT and shift the zero frequency to the center
    fourier = fftshift(fft2(windowed_pattern))
    
    # Get the center point
    N = pattern.shape[0]
    center = N // 2
    
    # Calculate how many pixels correspond to window_half_size
    # Since N/2 pixels = max_frequency in the FFT output
    # and max_frequency = pattern size/2
    # Therefore window_half_size pixels = (window_half_size * N) / pattern_size
    pixels = int((window_half_size * N) / (pattern.shape[0]))

    #set pixel value to 0 if it is outside the visibility radius using numpy and mesh 
    x = np.arange(-N // 2, N // 2)
    y = np.arange(-N // 2, N // 2)
    xx, yy = np.meshgrid(x, y)          
    distance = np.sqrt(xx**2 + yy**2)
    fourier_eaten = original_fourier.copy()
    fourier_eaten[distance > visibility_radius] = 0

    cropped_fourier = fourier[center-pixels:center+pixels, center-pixels:center+pixels] #Original fourier gets cropped
    cropped_fourier_eaten = fourier_eaten[center-pixels:center+pixels, center-pixels:center+pixels] #Eaten fourier gets cropped

    magnitude_spectrum = np.abs(cropped_fourier) # Magnitude spectrum is the absolute value of the cropped fourier
    
    magnitude_spectrum = (magnitude_spectrum - np.min(magnitude_spectrum)) / (  
        np.max(magnitude_spectrum) - np.min(magnitude_spectrum))    #Increase of contrast
    
    return cropped_fourier_eaten,magnitude_spectrum,

def compute_inverse_fourier(fourier_spectrum: np.ndarray) -> np.ndarray:
    """Compute the inverse Fourier transform."""
    # Unshift and apply inverse FFT
    inverse = np.real(ifft2(ifftshift(fourier_spectrum)))
    
    # Normalize
    inverse = (inverse - np.min(inverse)) / (np.max(inverse) - np.min(inverse))
    return inverse