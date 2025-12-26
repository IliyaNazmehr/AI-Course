import librosa
import numpy as np

def load_audio(file_path, duration=30):
    try:
        y, sr = librosa.load(file_path, duration=duration)
        return y, sr
    except Exception as e:
        raise RuntimeError(f"Error loading audio: {e}")

def extract_features(y, sr):
    mfccs = np.mean(librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13).T, axis=0)
    chroma = np.mean(librosa.feature.chroma_stft(y=y, sr=sr).T, axis=0)
    spectral_contrast = np.mean(
        librosa.feature.spectral_contrast(y=y, sr=sr).T, axis=0
    )
    tempo = librosa.beat.tempo(y=y, sr=sr)[0]
    mel_spec = np.mean(
        librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128).T, axis=0
    )

    return np.hstack([mfccs, chroma, spectral_contrast, tempo, mel_spec])

def extract_features_from_file(file_path):
    y, sr = load_audio(file_path)
    features = extract_features(y, sr)
    return features.reshape(1, -1)  # مهم برای مدل
