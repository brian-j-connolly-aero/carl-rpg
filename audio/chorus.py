import librosa
import numpy as np
import soundfile as sf


def pitch_shift_audio(input_file, output_file, n_steps=6):
    """
    Pitch shifts an audio file without changing its duration.
    Parameters:
    - input_file: Path to the input audio file.
    - output_file: Path where the output audio will be saved.
    - n_steps: Number of half-steps to shift the pitch. Positive values shift the pitch up, negative values shift it down.
    """
    # Load the audio file
    y, sr = librosa.load(input_file, sr=None)
    
    # Pitch shift the audio
    y_shifted = librosa.effects.pitch_shift(y, sr=sr, n_steps=n_steps)
    
    # Apply chorus effect
    y_chorused = apply_chorus(y_shifted, sr)
    
    # Save the pitch-shifted and chorused audio
    sf.write(output_file, y_chorused, sr)

def apply_chorus(y, sr, depth=0.005, rate=.1):
    """
    Applies a chorus effect to an audio signal.
    Parameters:
    - y: Audio signal as a numpy array.
    - sr: Sample rate of the audio signal.
    - depth: Chorus depth (default: 0.02).
    - rate: Chorus rate in Hz (default: 1.5).
    Returns:
    - y_chorused: Audio signal with chorus effect applied.
    """
    # Calculate the delay in samples
    delay_samples = int(depth * sr)
    
    # Create a delayed copy of the audio signal
    y_delayed = np.zeros_like(y)
    y_delayed[delay_samples:] = y[:-delay_samples]
    
    # Create a modulated delay
    lfo = np.sin(2 * np.pi * np.arange(len(y)) * rate / sr)
    mod_delay_samples = (depth / 2) * lfo * sr
    
    # Apply the modulated delay
    y_mod_delayed = np.zeros_like(y)
    for i in range(len(y)):
        idx = int(i - mod_delay_samples[i])
        if idx >= 0 and idx < len(y):
            y_mod_delayed[i] = y[idx]
    
    # Mix the original, delayed, and modulated signals
    y_chorused = y + y_delayed + y_mod_delayed
    
    # Normalize the output
    y_chorused /= np.max(np.abs(y_chorused))
    
    return y_chorused

if __name__=='__main__':
    # Example usage
    input_audio = 'cheevo_ai10.mp3'
    output_audio = 'cheevo_ai10_out.wav'
    n_steps = 4  # Shifts pitch up by 4 half-steps. Use negative values to shift down.
    #Audio should be elevenlabs patrick?
    pitch_shift_audio(input_audio, output_audio, n_steps)