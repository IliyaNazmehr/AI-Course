import os
import librosa
import numpy as np
import tensorflow_hub as hub
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
import joblib


# لود کردن مدل YAMNet
# (دقیقاً همونی که موقع پیش‌بینی استفاده می‌کنیم)
yamnet_model = hub.load("https://tfhub.dev/google/yamnet/1")

TARGET_SAMPLE_RATE = 16000


# استخراج ویژگی از یک فایل صوتی
def extract_audio_features(audio_file_path):
    """
    این تابع:
    - فایل صوتی رو لود می‌کنه
    - می‌فرستتش داخل YAMNet
    - در نهایت یک embedding عددی برمی‌گردونه
    """

    audio_signal, _ = librosa.load(
        audio_file_path,
        sr=TARGET_SAMPLE_RATE,
        mono=True
    )

    waveform = audio_signal.astype(np.float32)

    # خروجی YAMNet شامل score، embedding و spectrogram هست
    _, embeddings, _ = yamnet_model(waveform)

    # برای اینکه طول ویژگی‌ها ثابت باشه، میانگین می‌گیریم
    return np.mean(embeddings.numpy(), axis=0)


# ساخت دیتاست از فولدر ژانرها
def build_training_dataset(dataset_root_path):
    """
    ساخت X و y از ساختار فولدری دیتاست
    هر فولدر = یک ژانر
    """

    feature_vectors = []
    genre_labels = []

    for genre_name in os.listdir(dataset_root_path):
        genre_folder_path = os.path.join(dataset_root_path, genre_name)

        # اگه فایل بود یا فولدر نبود، بی‌خیالش می‌شیم
        if not os.path.isdir(genre_folder_path):
            continue

        for file_name in os.listdir(genre_folder_path):
            if not file_name.endswith(".wav"):
                continue

            audio_file_path = os.path.join(genre_folder_path, file_name)

            try:
                features = extract_audio_features(audio_file_path)
                feature_vectors.append(features)
                genre_labels.append(genre_name)

            except Exception as error:
                # اگه یه فایل خراب بود، کل آموزش نخوابه
                print(f"❌ Error while processing file {audio_file_path}: {error}")

    return np.array(feature_vectors), np.array(genre_labels)


# آموزش مدل
def main():
    print("📁 Building dataset...")

    X_features, y_genres = build_training_dataset(
        "data/genres_original"
    )

    print("🏷️ Encoding genre labels...")
    genre_label_encoder = LabelEncoder()
    y_encoded = genre_label_encoder.fit_transform(y_genres)

    print("📏 Scaling features...")
    feature_scaler = StandardScaler()
    X_scaled = feature_scaler.fit_transform(X_features)

    print("✂️ Splitting data into train and test sets...")
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled,
        y_encoded,
        test_size=0.2,
        random_state=42,
        stratify=y_encoded
    )

    print("🤖 Training SVM model...")
    svm_genre_model = SVC(
        kernel="rbf",
        C=10,
        gamma="scale",
        probability=True,        # برای اینکه بتونیم confidence حساب کنیم
        class_weight="balanced"  # جلوگیری از اینکه یه ژانر غالب بشه
    )

    svm_genre_model.fit(X_train, y_train)

    print(f"✅ Training accuracy: {svm_genre_model.score(X_train, y_train):.3f}")
    print(f"✅ Test accuracy:     {svm_genre_model.score(X_test, y_test):.3f}")

    # ذخیره همه چیز برای مرحله پیش‌بینی
    os.makedirs("model", exist_ok=True)
    joblib.dump(svm_genre_model, "model/svm_model.pkl")
    joblib.dump(feature_scaler, "model/scaler.pkl")
    joblib.dump(genre_label_encoder, "model/label_encoder.pkl")

    print("💾 Model, scaler, and label encoder saved successfully.")


if __name__ == "__main__":
    main()
