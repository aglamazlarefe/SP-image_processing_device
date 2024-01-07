import keras_ocr

# Keras-OCR, önyüklenmiş ağırlıkları otomatik olarak indirecek ve kullanacaktır.
pipeline = keras_ocr.pipeline.Pipeline()
keras_ocr.config.configure()  # Türkçe dilini kullanacak şekilde ayarlanmıştır.

# Üç örnek resim alalım
images = ["aligned_photo.jpg"]

# prediction_groups içindeki her liste, (word, box) demetlerinden oluşan bir liste.
prediction_groups = pipeline.recognize(images)

# Tahminleri ekrana yazdır
for image_path, predictions in zip(images, prediction_groups):
    print(f"{image_path} için Tahminler:")
    for word, box in predictions:
        print(f"Kelime: {word}")
    print()
