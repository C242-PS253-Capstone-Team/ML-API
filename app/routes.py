from flask import Blueprint, request, jsonify
import tensorflow as tf
import numpy as np
from PIL import Image
from io import BytesIO

main_bp = Blueprint('main', __name__)

# Load model
try:
    model = tf.keras.models.load_model('app/model/model.h5')
    print("Model successfully loaded.")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None  # Inisialisasi model sebagai None jika gagal dimuat

# Fungsi preprocessing dan prediksi gambar
def predict_image(image_data):
    try:
        # Load image menggunakan Pillow dan resize gambar ke 224x224
        img = Image.open(BytesIO(image_data)).convert("RGB").resize((224, 224))
    except Exception as e:
        return {"error": f"Error loading image: {e}"}, 500

    # Preprocessing gambar
    img_array = np.array(img) / 255.0  # Normalisasi gambar
    img_array = np.expand_dims(img_array, axis=0)  # Menambahkan dimensi batch

    # Prediksi menggunakan model
    prediction = model.predict(img_array)

    # Menghitung probabilitas untuk setiap kelas
    pred_scores = prediction[0]  # Ambil skor probabilitas untuk gambar pertama

    # Urutkan probabilitas secara menurun dan ambil 5 kelas tertinggi
    top_5_classes_idx = np.argsort(pred_scores)[-5:][::-1]
    top_5_confidence = [float(pred_scores[idx]) for idx in top_5_classes_idx]

    # Label untuk setiap gaya rambut berdasarkan index
    hairstyle_labels = ["Oblong", "Heart", "Round", "Square", "Oval"]  # 5 kelas gaya rambut
    
    # Ambil nama kelas dan confidence untuk 5 kelas tertinggi
    predicted_class_names = [hairstyle_labels[idx] for idx in top_5_classes_idx]
    
    # Membuat dictionary dengan kelas sebagai key dan confidence sebagai value
    confidence_dict = {predicted_class_names[i].lower(): top_5_confidence[i] for i in range(len(predicted_class_names))}

    # Urutkan dictionary berdasarkan confidence (nilai tertinggi ke terendah)
    sorted_confidence_dict = dict(sorted(confidence_dict.items(), key=lambda item: item[1], reverse=True))

    return {"predict": sorted_confidence_dict}

@main_bp.route("/predict", methods=["POST"])
def predict():
    if "picture" not in request.files:
        return jsonify({"error": "No picture uploaded"}), 400

    picture = request.files["picture"]

    if picture.filename == "":
        return jsonify({"error": "No selected picture"}), 400

    # Cek jika file gambar memiliki ekstensi yang valid
    if not picture.filename.lower().endswith((".png", ".jpg", ".jpeg")):
        return jsonify({"error": "Invalid image file format"}), 400

    if picture:
        # Mendapatkan data gambar
        image_data = picture.read()

        # Mendapatkan prediksi dari gambar yang diupload
        prediction = predict_image(image_data)

        # Mengembalikan hasil prediksi sebagai JSON
        return jsonify(prediction)
