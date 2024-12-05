# from PIL import Image
# import numpy as np
# import io

# def prepare_image(image):
#     # Membaca gambar dari byte stream
#     img = Image.open(io.BytesIO(image))
    
#     # Mengubah ukuran gambar sesuai dengan input model
#     img = img.resize((224, 224))  # Sesuaikan ukuran gambar dengan model yang dilatih
    
#     # Normalisasi gambar
#     img = np.array(img) / 255.0  # Membagi dengan 255 agar pixel value dalam rentang 0-1
    
#     # Menambahkan dimensi batch (sebagai input model)
#     img = np.expand_dims(img, axis=0)
    
#     return img
