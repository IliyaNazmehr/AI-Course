import librosa
import numpy as np
import tensorflow_hub as hub
import joblib
import os


# ثابت‌های کلی پروژه
SAMPLE_RATE = 16000              # نرخ نمونه‌برداری استاندارد برای YAMNet
MODEL_DIR = "model"              # پوشه‌ای که مدل و فایل‌های مربوطه داخلش ذخیره میشن

MODEL_PATH = os.path.join(MODEL_DIR, "svm_model.pkl")
SCALER_PATH = os.path.join(MODEL_DIR, "scaler.pkl")
ENCODER_PATH = os.path.join(MODEL_DIR, "label_encoder.pkl")


# بارگذاری مدل YAMNet
# این مدل از قبل train شده و فقط برای استخراج ویژگی استفاده میشه
YAMNET = hub.load("https://tfhub.dev/google/yamnet/1")


# متغیرهای lazy-load شده
# اینا اولش None هستن و فقط وقتی لازم بشه load میشن
svm_model = None
scaler = None
label_encoder = None


def load_model_if_needed():
    """
    این تابع فقط وقتی مدل واقعاً لازم باشه
    فایل‌های train شده رو از دیسک load می‌کنه
    (برای جلوگیری از load شدن بی‌مورد موقع اجرای UI)
    """
    global svm_model, scaler, label_encoder

    # اگر قبلاً load شده، دیگه کاری نکن
    if svm_model is not None:
        return

    # اگر مدل وجود نداشته باشه یعنی هنوز train نشده
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError("Model is not trained yet")

    # load کردن فایل‌های ذخیره‌شده
    svm_model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    label_encoder = joblib.load(ENCODER_PATH)


# استخراج ویژگی با YAMNet
def extract_yamnet_features(audio_path, progress_callback=None):
    """
    این تابع فایل صوتی رو می‌گیره،
    می‌فرسته به YAMNet
    و embedding نهایی رو برمی‌گردونه
    """
    # لود فایل صوتی و تبدیل به mono
    audio, _ = librosa.load(audio_path, sr=SAMPLE_RATE, mono=True)
    waveform = audio.astype(np.float32)

    # گرفتن embedding از YAMNet
    scores, embeddings, _ = YAMNET(waveform)

    # برای آپدیت progress (اینجا فقط یه مرحله داریم)
    if progress_callback:
        progress_callback(1, 1)

    # میانگین گرفتن از embedding‌ها برای یک بردار نهایی
    return np.mean(embeddings.numpy(), axis=0)


# پیش‌بینی ژانر به همراه confidence
def predict_genre_with_confidence(audio_path, progress_callback=None):
    """
    این تابع ژانر آهنگ رو پیش‌بینی می‌کنه
    و درصد اطمینان هر ژانر رو هم برمی‌گردونه
    """

    # 🔴 اول مطمئن میشیم مدل load شده
    load_model_if_needed()

    # استخراج ویژگی از فایل صوتی
    features = extract_yamnet_features(
        audio_path,
        progress_callback
    )

    # نرمال‌سازی ویژگی‌ها با اسکیلری که موقع train استفاده شده
    features = scaler.transform([features])

    # گرفتن احتمال هر کلاس از SVM
    probabilities = svm_model.predict_proba(features)[0]

    # ایندکس ژانری که بیشترین احتمال رو داره
    predicted_index = np.argmax(probabilities)

    # تبدیل لیبل عددی به اسم ژانر
    predicted_genre = label_encoder.inverse_transform(
        [predicted_index]
    )[0]

    # ساخت دیکشنری confidence برای نمایش در UI
    confidence_dict = {
        label_encoder.inverse_transform([i])[0]: prob
        for i, prob in enumerate(probabilities)
    }

    return predicted_genre, confidence_dict
