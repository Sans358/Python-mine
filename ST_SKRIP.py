import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
import streamlit as st
import pandas as pd
import cv2
import numpy as np
from PIL import Image
from tensorflow.keras.models import load_model

# Memuat model yang sudah dilatih
model_path = "best_model.h5"
model = load_model(model_path, compile=False)
classes = ["Mengelupas", "Normal", "Pecah"]

# Fungsi untuk melakukan preprocessing pada citra
def preprocess(image):
    resized = cv2.resize(image, (224, 224))
    normalized = resized / 255.0
    return np.expand_dims(normalized, axis=0)

# Fungsi utama aplikasi
def main():
    # Menampilkan judul aplikasi
    st.title("SISTEM IDENTIFIKASI KUALITAS KEDELAI MENGGUNAKAN TRANSFER LEARNING MOBILENETV2")
    
    uploaded = st.file_uploader("Pilih file gambar", type=["jpg", "jpeg", "png"])
    
    if uploaded is not None:
        # Menampilkan gambar yang diunggah
        image = Image.open(uploaded)
        st.image(image, caption="Citra Input", use_column_width=True)
        
        # Konversi gambar ke format yang bisa diproses oleh OpenCV
        image = np.array(image)
        if image.shape[-1] == 4:  # Jika gambar memiliki kanal alpha, konversi ke RGB
            image = cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)
        
        # Proses gambar
        processed = preprocess(image)
        predictions = model.predict(processed)
        predictions_df = pd.DataFrame(predictions, columns=classes)
        
        # Menampilkan prediksi di bagian bawah gambar
        col1, col2 = st.columns(2)
        
        with col1:
            st.write(f"{classes[0]}: {predictions_df.iloc[0][0]:.2%}")
            st.write(f"{classes[1]}: {predictions_df.iloc[0][1]:.2%}")
            st.write(f"{classes[2]}: {predictions_df.iloc[0][2]:.2%}")
        
        with col2:
            class_prob = predictions_df.iloc[0].tolist()
            predicted_index = np.argmax(class_prob)
            predicted_class = classes[predicted_index]
            st.subheader("Prediksi:")
            st.subheader(predicted_class)
    else:
        st.write("Silakan unggah gambar untuk memulai prediksi.")

if __name__ == "__main__":
    main()