# -------------------------------------------------------------------
# PROGRAM PYTHON KOMPREHENSIF - PENGOLAHAN CITRA DIGITAL
# Materi: PERTEMUAN 7 - DETEKSI TEPI DAN SEGMENTASI WARNA
# Ryan Hidayat.
#
# Program ini akan mendemonstrasikan 5 teknik:
# 1. Deteksi Tepi - Sobel
# 2. Deteksi Tepi - Prewitt
# 3. Deteksi Tepi - Canny
# 4. Segmentasi Warna - K-Means Clustering
# 5. Segmentasi Warna - Thresholding HSV
# -------------------------------------------------------------------

import cv2
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans


# --- FUNGSI BANTU UNTUK MENAMPILKAN GAMBAR ---
# Dibuat agar lebih rapi saat menampilkan banyak gambar
def tampilkan_hasil(judul_jendela, daftar_gambar, baris, kolom):
    """
    Fungsi helper untuk menampilkan beberapa gambar menggunakan Matplotlib.

    Args:
        judul_jendela (str): Judul untuk jendela plot.
        daftar_gambar (list): List berisi tuple (judul_gambar, gambar).
        baris (int): Jumlah baris di subplot.
        kolom (int): Jumlah kolom di subplot.
    """
    plt.figure(figsize=(kolom * 5, baris * 4))
    plt.suptitle(judul_jendela, fontsize=16)

    for i, (judul, gambar) in enumerate(daftar_gambar):
        plt.subplot(baris, kolom, i + 1)
        plt.title(judul)

        # Cek apakah gambar grayscale atau color
        if len(gambar.shape) == 2:
            plt.imshow(gambar, cmap='gray')
        else:
            # Asumsikan gambar dalam format RGB untuk matplotlib
            plt.imshow(gambar)

        plt.axis('off')

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()


# --- FUNGSI UTAMA (MAIN) ---
def main():
    # --- 1. PERSIAPAN DAN MEMBACA CITRA ---
    nama_file_gambar = 'react_idle.png'  # Coba gunakan gambar 'gw.jpg' atau 'kota4.png' dari dokuenm

    # Membaca citra dalam mode WARNA (BGR)
    image_bgr = cv2.imread(nama_file_gambar)



    # Konversi ke RGB untuk Matplotlib dan K-Means [cite: 274, 382]
    image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)

    # Konversi ke Grayscale untuk Deteksi Tepi [cite: 20]
    image_gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)

    print("Memproses gambar...")

    # =================================================================
    # BAGIAN A: DETEKSI TEPI (SOBEL, PREWITT, CANNY)
    # =================================================================

    # --- 2. DETEKSI TEPI - OPERATOR SOBEL [cite: 10, 33] ---
    # Terapkan Sobel X dan Y [cite: 34, 35]
    sobel_x = cv2.Sobel(image_gray, cv2.CV_64F, 1, 0, ksize=5)
    sobel_y = cv2.Sobel(image_gray, cv2.CV_64F, 0, 1, ksize=5)
    # Hitung magnitudo [cite: 36]
    sobel_magnitude = np.sqrt(sobel_x ** 2 + sobel_y ** 2)
    sobel_hasil = cv2.convertScaleAbs(sobel_magnitude)  # [cite: 38]

    # --- 3. DETEKSI TEPI - OPERATOR PREWITT [cite: 75, 98] ---
    # Definisikan kernel Prewitt
    kernel_prewitt_x = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]], dtype=np.float32)
    kernel_prewitt_y = np.array([[1, 1, 1], [0, 0, 0], [-1, -1, -1]], dtype=np.float32)

    # Terapkan filter Prewitt X dan Y
    prewitt_x = cv2.filter2D(image_gray.astype(np.float32), -1, kernel_prewitt_x)
    prewitt_y = cv2.filter2D(image_gray.astype(np.float32), -1, kernel_prewitt_y)

    # Hitung magnitudo [cite: 111]
    prewitt_magnitude = np.sqrt(prewitt_x ** 2 + prewitt_y ** 2)
    prewitt_hasil = cv2.convertScaleAbs(prewitt_magnitude)  # [cite: 113]

    # --- 4. DETEKSI TEPI - METODE CANNY [cite: 167, 195] ---
    # Terapkan Canny dengan threshold medium
    canny_hasil = cv2.Canny(image_gray, threshold1=100, threshold2=200)

    # --- 5. TAMPILKAN HASIL DETEKSI TEPI ---
    daftar_gambar_tepi = [
        ('Citra Asli (Grayscale)', image_gray),
        ('Hasil Sobel', sobel_hasil),
        ('Hasil Prewitt', prewitt_hasil),
        ('Hasil Canny', canny_hasil)
    ]
    tampilkan_hasil('Hasil Deteksi Tepi (Pertemuan 7)', daftar_gambar_tepi, 2, 2)

    # =================================================================
    # BAGIAN B: SEGMENTASI WARNA (K-MEANS, THRESHOLDING)
    # =================================================================

    # --- 6. SEGMENTASI WARNA - K-MEANS CLUSTERING [cite: 253, 290] ---
    # Ubah bentuk citra menjadi 2D (jumlah_piksel, 3)
    pixel_values = image_rgb.reshape((-1, 3))
    pixel_values = np.float32(pixel_values)  # [cite: 292]

    # Tentukan jumlah cluster (K)
    k = 4  # [cite: 294, 313] (Contoh K=4)

    # Terapkan K-Means [cite: 295]
    kmeans = KMeans(n_clusters=k, random_state=0, n_init=10)
    kmeans.fit(pixel_values)  #

    # Ganti piksel dengan warna centroid-nya [cite: 298]
    segmented_colors = kmeans.cluster_centers_[kmeans.labels_]
    # Ubah kembali ke bentuk citra asli [cite: 299, 351]
    kmeans_hasil = segmented_colors.reshape(image_rgb.shape).astype(np.uint8)

    # --- 7. SEGMENTASI WARNA - THRESHOLDING HSV [cite: 364, 399] ---
    # Konversi citra RGB ke HSV
    image_hsv = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2HSV)

    # Tentukan rentang warna (Contoh: warna hijau) [cite: 402, 403]
    # H: 0-180, S: 0-255, V: 0-255 di OpenCV
    lower_hijau = np.array([35, 40, 40])
    upper_hijau = np.array([85, 255, 255])

    # Buat masker (mask)
    hsv_mask = cv2.inRange(image_hsv, lower_hijau, upper_hijau)

    # Terapkan masker ke citra asli (RGB)
    threshold_hasil = cv2.bitwise_and(image_rgb, image_rgb, mask=hsv_mask)

    # --- 8. TAMPILKAN HASIL SEGMENTASI WARNA ---
    daftar_gambar_segmentasi = [
        ('Citra Asli (RGB)', image_rgb),
        (f'Hasil K-Means (K={k})', kmeans_hasil),
        ('Masker HSV (Hijau)', hsv_mask),
        ('Hasil Thresholding (Hijau)', threshold_hasil)
    ]
    tampilkan_hasil('Hasil Segmentasi Warna (Pertemuan 7)', daftar_gambar_segmentasi, 2, 2)

    print("Semua proses selesai.")


# --- PANGGIL FUNGSI UTAMA ---
if __name__ == "__main__":
    main()