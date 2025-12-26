import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from predict import predict_genre_with_confidence
import os
import threading
import subprocess


# لیست برای نگهداری تاریخچه آهنگ‌هایی که پردازش شدن
song_history = []


# هندلر آموزش مدل (Train)
def handle_train_model():
    """
    این تابع وقتی دکمه Train Model زده میشه اجرا میشه
    آموزش مدل رو داخل یه thread جدا انجام میده
    تا UI قفل نشه
    """
    def run_training():
        try:
            # غیر فعال کردن دکمه Train موقع آموزش
            train_button.config(state="disabled")
            status_label.config(text="Training model... Please wait")

            # اجرای فایل train_model.py
            subprocess.run(
                ["python", "train_model.py"],
                check=True
            )

            # بعد از اتمام موفق
            status_label.config(text="Model trained successfully")
            messagebox.showinfo(
                "Training Completed",
                "Model training finished successfully.\nYou can now predict genres."
            )

        except subprocess.CalledProcessError:
            # اگر حین train خطا پیش بیاد
            messagebox.showerror(
                "Training Failed",
                "An error occurred during model training."
            )

        finally:
            # فعال کردن دوباره دکمه Train
            train_button.config(state="normal")

    # اجرای آموزش داخل Thread
    training_thread = threading.Thread(target=run_training)
    training_thread.start()


# انتخاب فایل موسیقی و پیش‌بینی ژانر
def handle_file_selection():
    """
    انتخاب فایل صوتی و ارسالش به مدل برای پیش‌بینی ژانر
    """
    audio_file_path = filedialog.askopenfilename(
        filetypes=[("Audio Files", "*.wav *.mp3")]
    )

    if not audio_file_path:
        return

    # اسم آهنگ بدون پسوند
    track_name = os.path.splitext(
        os.path.basename(audio_file_path)
    )[0]

    # ریست کردن UI
    result_label.config(text="")
    confidence_box.delete("1.0", tk.END)
    status_label.config(text=f"Processing: {track_name}")
    progress_bar["value"] = 0
    main_window.update()

    # تابع آپدیت نوار پیشرفت
    def update_progress_ui(current, total):
        percent = int((current / total) * 100)
        progress_bar["value"] = percent
        status_label.config(
            text=f"Processing '{track_name}' ... {percent}%"
        )
        main_window.update()

    try:
        # گرفتن خروجی مدل
        predicted_genre, confidence_scores = predict_genre_with_confidence(
            audio_file_path,
            progress_callback=update_progress_ui
        )

        status_label.config(text="Processing completed")

        # نمایش نتیجه اصلی
        result_label.config(
            text=f"🎵 {track_name}\n🎧 Genre: {predicted_genre}"
        )

        # نمایش درصد اطمینان هر ژانر
        confidence_box.delete("1.0", tk.END)
        for genre, score in sorted(
            confidence_scores.items(),
            key=lambda x: x[1],
            reverse=True
        ):
            confidence_box.insert(
                tk.END,
                f"{genre}: {score * 100:.2f}%\n"
            )

        # ذخیره نتیجه در تاریخچه
        song_history.append({
            "track_name": track_name,
            "predicted_genre": predicted_genre,
            "confidence_scores": confidence_scores
        })

        history_listbox.insert(
            tk.END,
            f"{track_name}  →  {predicted_genre}"
        )

    except FileNotFoundError:
        # اگر مدل هنوز train نشده باشه
        messagebox.showerror(
            "Model Not Trained",
            "Model is not trained yet.\nPlease train the model first."
        )

    except Exception as error:
        # خطاهای عمومی
        status_label.config(text="Error")
        messagebox.showerror("Error", str(error))


# کلیک روی آیتم‌های تاریخچه
def handle_history_selection(event):
    """
    وقتی کاربر روی یکی از آهنگ‌های تاریخچه کلیک می‌کنه
    اطلاعات همون آهنگ دوباره نمایش داده میشه
    """
    selected_index = history_listbox.curselection()
    if not selected_index:
        return

    item = song_history[selected_index[0]]

    result_label.config(
        text=f"{item['track_name']}\nGenre: {item['predicted_genre']}"
    )

    confidence_box.delete("1.0", tk.END)
    for genre, score in sorted(
        item["confidence_scores"].items(),
        key=lambda x: x[1],
        reverse=True
    ):
        confidence_box.insert(
            tk.END,
            f"{genre}: {score * 100:.2f}%\n"
        )


# تنظیمات کلی رابط گرافیکی
main_window = tk.Tk()
main_window.title("Tune Sense")
main_window.geometry("760x480")
main_window.resizable(False, False)


# پنل سمت چپ (کنترل اصلی)
left_panel = tk.Frame(main_window)
left_panel.pack(side="left", padx=10)

title_label = tk.Label(
    left_panel,
    text="Tune Sense",
    font=("Arial", 18, "bold")
)
title_label.pack(pady=10)


train_button = tk.Button(
    left_panel,
    text="Train Model",
    font=("Arial", 12),
    width=24,
    command=handle_train_model
)
train_button.pack(pady=6)

select_button = tk.Button(
    left_panel,
    text="Select Music File",
    font=("Arial", 12),
    width=24,
    command=handle_file_selection
)
select_button.pack(pady=6)

progress_bar = ttk.Progressbar(
    left_panel,
    length=400,
    mode="determinate"
)
progress_bar.pack(pady=8)

status_label = tk.Label(
    left_panel,
    text="",
    font=("Arial", 11),
    fg="blue"
)
status_label.pack(pady=6)

result_label = tk.Label(
    left_panel,
    text="",
    font=("Arial", 14),
    fg="green",
    justify="center"
)
result_label.pack(pady=10)

confidence_box = tk.Text(
    left_panel,
    height=8,
    width=48,
    font=("Arial", 11)
)
confidence_box.pack(pady=10)


# پنل سمت راست (تاریخچه)
right_panel = tk.Frame(main_window)
right_panel.pack(side="right", fill="y", padx=10)

history_title = tk.Label(
    right_panel,
    text="History",
    font=("Arial", 14, "bold")
)
history_title.pack(pady=10)

history_frame = tk.Frame(right_panel)
history_frame.pack()

# اسکرول عمودی و افقی
scroll_y = tk.Scrollbar(history_frame, orient="vertical")
scroll_x = tk.Scrollbar(history_frame, orient="horizontal")

history_listbox = tk.Listbox(
    history_frame,
    width=34,
    height=18,
    yscrollcommand=scroll_y.set,
    xscrollcommand=scroll_x.set
)

scroll_y.config(command=history_listbox.yview)
scroll_x.config(command=history_listbox.xview)

history_listbox.grid(row=0, column=0, sticky="nsew")
scroll_y.grid(row=0, column=1, sticky="ns")
scroll_x.grid(row=1, column=0, sticky="ew")

history_listbox.bind(
    "<<ListboxSelect>>",
    handle_history_selection
)

# جلوگیری از انتخاب خودکار متن
history_listbox.config(exportselection=False)

main_window.mainloop()
