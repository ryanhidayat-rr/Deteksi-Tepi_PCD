### PENJELASAN SINGKAT MATERI DETEKSI TEPI DAN SEGMENTASI WARNA

### Deteksi Tepi (Edge Detection)
Deteksi Tepi adalah sebuah proses dalam pengolahan citra untuk mengidentifikasi dan menemukan lokasi di mana terdapat batas-batas atau kontur objek dalam sebuah gambar. Cara kerjanya adalah dengan mendeteksi area di mana terjadi perubahan intensitas (kecerahan) piksel yang drastis atau tiba-tiba. Tujuannya adalah untuk menyederhanakan gambar, hanya menyisakan garis-garis penting yang mewakili bentuk objek. Metode yang umum digunakan adalah Sobel, Prewitt, dan Canny.

### Segmentasi Warna (Color Segmentation)
Segmentasi Warna adalah proses untuk mempartisi atau membagi sebuah gambar digital menjadi beberapa wilayah (segmen) yang berbeda berdasarkan kesamaan karakteristik warnanya. Cara kerjanya adalah dengan mengelompokkan piksel-piksel yang memiliki warna serupa ke dalam satu grup atau segmen yang sama. Tujuannya bisa untuk menyederhanakan gambar (mengurangi palet warna) atau untuk mengisolasi objek tertentu yang memiliki warna spesifik. Metode yang umum digunakan adalah K-Means Clustering dan Thresholding (seringkali di ruang warna HSV).### Pengolahan Citra Digital: Deteksi Tepi dan Segmentasi Warna.

### 1. Persiapan Awal (di dalam fungsi `main`)
* Impor Library: Skrip ini mengimpor beberapa pustaka: `cv2` (OpenCV) untuk fungsi pemrosesan gambar, `numpy` untuk operasi array, `matplotlib.pyplot` untuk visualisasi data (plotting gambar), dan `KMeans` dari `scikit-learn` untuk clustering.
* Membaca Gambar: `cv2.imread` digunakan untuk memuat sebuah file gambar. Penting dicatat bahwa OpenCV memuat gambar dalam format BGR (Blue-Green-Red).
* Konversi Ruang Warna: Ini adalah langkah krusial.
    * `image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)`: Gambar dikonversi dari BGR ke RGB. Ini diperlukan karena Matplotlib dan K-Means mengharapkan format RGB.
    * `image_gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)`: Sebuah versi grayscale (keabuan) dari gambar dibuat. Ini adalah input standar untuk banyak algoritma deteksi tepi, karena mereka bekerja berdasarkan perbedaan intensitas cahaya, bukan warna.

---

### Bagian A: Deteksi Tepi

Tujuan deteksi tepi adalah menemukan lokasi di mana intensitas piksel berubah secara drastis, yang biasanya menandakan sebuah batas.

#### 2. Deteksi Tepi - Sobel

* Konsep: Operator Sobel menghitung gradien (turunan) dari intensitas gambar. Ini mengukur seberapa cepat intensitas piksel berubah ke arah horizontal (X) dan vertikal (Y).
* Cara Kerja:
    * `cv2.Sobel(..., 1, 0, ...)` menghitung gradien pada sumbu X, yang efektif untuk mendeteksi tepi vertikal.
    * `cv2.Sobel(..., 0, 1, ...)` menghitung gradien pada sumbu Y, untuk mendeteksi tepi horizontal.
    * `np.sqrt(sobel_x ** 2 + sobel_y ** 2)` adalah rumus matematika untuk menghitung magnitudo (kekuatan) total gradien, menggabungkan hasil X dan Y.
    * `cv2.convertScaleAbs` mengubah hasil perhitungan, yang mungkin berupa angka non-integer, kembali ke format gambar 8-bit (nilai 0-255) agar bisa ditampilkan.

#### 3. Deteksi Tepi - Prewitt

* Konsep: Mirip dengan Sobel, Prewitt juga operator berbasis gradien. Perbedaannya hanya terletak pada nilai-nilai di dalam matriks kecil (kernel) yang digunakannya untuk menghitung gradien.
* Cara Kerja:
    * Tidak seperti Sobel yang punya fungsi bawaan, di sini kernel Prewitt (`kernel_prewitt_x` dan `kernel_prewitt_y`) didefinisikan secara manual sebagai array NumPy.
    * `cv2.filter2D` adalah fungsi yang lebih umum untuk menerapkan filter atau kernel kustom ke sebuah gambar.
    * Perhitungan magnitudo dan konversi skalanya identik dengan metode Sobel.

#### 4. Deteksi Tepi - Canny

* Konsep: Ini adalah metode deteksi tepi yang lebih canggih dan dianggap sebagai standar emas. Ini adalah algoritma multi-tahap yang menghasilkan tepi yang tipis dan bersih dengan lebih sedikit noise.
* Cara Kerja (Internal `cv2.Canny`):
    1.  Reduksi Noise: Menggunakan filter Gaussian Blur untuk menghaluskan gambar.
    2.  Gradien: Menggunakan Sobel untuk menemukan kekuatan dan arah gradien.
    3.  Non-Maximum Suppression: Menipiskan tepi menjadi satu piksel saja.
    4.  Hysteresis Thresholding: Menggunakan dua nilai ambang (rendah dan tinggi) untuk menentukan tepi. Tepi yang kuat (di atas ambang tinggi) akan dipertahankan. Tepi yang lemah (di bawah ambang rendah) akan dibuang. Tepi yang berada di antaranya hanya akan dipertahankan jika terhubung dengan tepi yang kuat.

---

### Bagian B: Segmentasi Warna

Tujuan segmentasi adalah membagi gambar menjadi beberapa wilayah berdasarkan karakteristik tertentu, dalam hal ini warna.

#### 6. Segmentasi Warna - K-Means Clustering

* Konsep: Ini adalah algoritma *unsupervised machine learning*. Tujuannya adalah untuk menemukan `k` warna "pusat" (centroid) yang paling mewakili semua warna dalam gambar. Setiap piksel kemudian akan diganti warnanya dengan warna centroid yang paling mirip.
* Cara Kerja:
    1.  `pixel_values = image_rgb.reshape((-1, 3))`: Gambar (misal: 100x100 piksel) diubah bentuknya dari (100, 100, 3) menjadi (10000, 3). Ini menciptakan daftar panjang berisi semua piksel.
    2.  `kmeans = KMeans(n_clusters=k, ...)`: Menginisialisasi algoritma, memberitahunya untuk mencari `k` cluster (dalam kode ini, `k=4`).
    3.  `kmeans.fit(pixel_values)`: Algoritma "belajar" dari data piksel dan menemukan 4 warna pusat (centroid) terbaik.
    4.  `segmented_colors = kmeans.cluster_centers_[kmeans.labels_]`: Ini adalah langkah utamanya. `kmeans.labels_` berisi label (0, 1, 2, atau 3) untuk setiap piksel. Baris ini "mewarnai ulang" setiap piksel dengan warna centroid yang sesuai dengan labelnya.
    5.  `...reshape(image_rgb.shape)`: Data piksel yang sudah disederhanakan warnanya diubah kembali ke bentuk gambar aslinya.

#### 7. Segmentasi Warna - Thresholding HSV

* Konsep: Ini adalah metode berbasis aturan yang lebih sederhana untuk mengisolasi satu rentang warna tertentu (misalnya, semua nuansa hijau).
* Cara Kerja:
    1.  `image_hsv = cv2.cvtColor(..., cv2.COLOR_RGB2HSV)`: Gambar diubah ke ruang warna HSV (Hue, Saturation, Value).
    2.  Mengapa HSV? Ruang warna ini memisahkan warna murni (Hue) dari kepekatan (Saturation) dan kecerahan (Value). Ini membuat pemilihan warna (seperti "hijau") jauh lebih mudah dan lebih andal daripada di RGB.
    3.  `lower_hijau` dan `upper_hijau`: Mendefinisikan rentang nilai H, S, dan V yang dianggap sebagai "hijau".
    4.  `hsv_mask = cv2.inRange(...)`: Ini adalah fungsi kunci. Ia membuat gambar hitam-putih (disebut *mask*). Piksel yang warnanya berada *di dalam* rentang yang ditentukan menjadi putih, dan yang di luar rentang menjadi hitam.
    5.  `threshold_hasil = cv2.bitwise_and(...)`: Operasi ini menggunakan masker untuk "menyaring" gambar asli. Ia hanya akan mempertahankan piksel dari gambar asli di lokasi di mana maskernya berwarna putih.
