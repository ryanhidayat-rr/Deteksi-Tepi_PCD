Tentu, ini adalah program Python yang sangat bagus untuk mendemonstrasikan dasar-dasar Pengolahan Citra Digital. Mari saya jelaskan alur kerja dan konsep di balik setiap bagian kode Anda.

### Penjelasan Umum

Program ini dibagi menjadi dua bagian utama, sesuai dengan materi pertemuannya:

1.  **Bagian A: Deteksi Tepi (Edge Detection)**
    * Tujuannya adalah untuk mengidentifikasi batas-batas atau kontur objek dalam sebuah gambar.
    * Ini dilakukan dengan menemukan area di mana intensitas (kecerahan) piksel berubah secara drastis.
    * Program ini mendemonstrasikan tiga metode: **Sobel**, **Prewitt**, dan **Canny**.

2.  **Bagian B: Segmentasi Warna (Color Segmentation)**
    * Tujuannya adalah untuk mempartisi atau membagi gambar menjadi beberapa wilayah (segmen) berdasarkan kesamaan warna.
    * Ini berguna untuk mengisolasi objek tertentu atau menyederhanakan gambar.
    * Program ini mendemonstrasikan dua metode: **K-Means Clustering** dan **Thresholding HSV**.

Program ini juga menggunakan fungsi pembantu (`tampilkan_hasil`) yang sangat baik, yang menggunakan `matplotlib` untuk menampilkan beberapa gambar dalam satu jendela plot yang rapi.

---

### Cara Kerja Program (Langkah demi Langkah)

Berikut adalah rincian dari apa yang dilakukan oleh setiap blok kode:

#### 1. Persiapan Awal (di dalam `main`)

1.  **Impor Library:** Program mengimpor `cv2` (OpenCV untuk pemrosesan gambar), `numpy` (untuk operasi numerik dan array), `matplotlib.pyplot` (untuk menampilkan gambar), dan `KMeans` (dari `scikit-learn` untuk clustering).
2.  **Membaca Gambar:** `cv2.imread(nama_file_gambar)` memuat gambar dari file. Penting untuk dicatat bahwa OpenCV memuat gambar dalam format **BGR** (Blue-Green-Red), bukan RGB.
3.  **Konversi Ruang Warna:**
    * `image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)`: Gambar dikonversi ke **RGB**. Ini penting karena `matplotlib` dan `scikit-learn` (K-Means) mengharapkan format RGB.
    * `image_gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)`: Gambar dikonversi ke **Grayscale** (skala keabuan). Ini adalah langkah yang wajib untuk sebagian besar algoritma deteksi tepi (Sobel, Prewitt, Canny), karena mereka bekerja berdasarkan perbedaan *intensitas* cahaya, bukan warna.

---

### Bagian A: Deteksi Tepi

#### 2. Deteksi Tepi - Sobel

* **Konsep:** Operator Sobel adalah operator turunan (derivatif) orde pertama. Ia menghitung gradien (tingkat perubahan) intensitas piksel.
* **Cara Kerja:**
    * `cv2.Sobel(..., 1, 0, ...)`: Menghitung gradien pada sumbu **X** (mendeteksi tepi vertikal).
    * `cv2.Sobel(..., 0, 1, ...)`: Menghitung gradien pada sumbu **Y** (mendeteksi tepi horizontal).
    * `np.sqrt(sobel_x ** 2 + sobel_y ** 2)`: Menghitung **magnitudo** (besaran) total dari gradien. Ini menggabungkan tepi vertikal dan horizontal menjadi satu.
    * `cv2.convertScaleAbs(...)`: Mengonversi hasilnya kembali ke tipe data `uint8` (0-255) agar dapat ditampilkan sebagai gambar.

#### 3. Deteksi Tepi - Prewitt

* **Konsep:** Sangat mirip dengan Sobel, Prewitt juga merupakan operator turunan orde pertama. Perbedaannya hanya terletak pada nilai *kernel* (matriks 3x3) yang digunakannya.
* **Cara Kerja:**
    * Tidak seperti Sobel yang memiliki fungsi bawaan `cv2.Sobel`, di sini Anda mendefinisikan kernel Prewitt secara manual (`kernel_prewitt_x` dan `kernel_prewitt_y`).
    * `cv2.filter2D(...)`: Fungsi ini menerapkan *filter* (kernel) kustom ke gambar. Ini adalah cara manual untuk melakukan apa yang dilakukan `cv2.Sobel`.
    * Perhitungan magnitudo dan konversi skalanya sama persis dengan Sobel.

#### 4. Deteksi Tepi - Canny

* **Konsep:** Canny adalah metode deteksi tepi yang paling canggih dan populer. Ini adalah algoritma multi-tahap yang menghasilkan tepi yang sangat bersih dan tipis.
* **Cara Kerja (Internal `cv2.Canny`):**
    1.  **Reduksi Noise:** Menerapkan filter Gaussian Blur untuk menghaluskan gambar dan menghilangkan noise.
    2.  **Perhitungan Gradien:** Menggunakan operator Sobel untuk menemukan gradien intensitas.
    3.  **Non-Maximum Suppression:** Menipiskan tepi. Hanya piksel yang merupakan gradien terkuat di lingkungannya yang dipertahankan.
    4.  **Hysteresis Thresholding:** Ini adalah bagian yang paling cerdas. Ia menggunakan dua nilai *threshold* (ambang batas):
        * `threshold2` (tinggi): Piksel di atas ini pasti dianggap sebagai tepi.
        * `threshold1` (rendah): Piksel di bawah ini pasti dibuang.
        * Piksel di antara keduanya *hanya* akan dianggap sebagai tepi jika mereka terhubung ke piksel yang berada di atas `threshold2`. Ini membantu menyambung tepi yang putus-putus.

---

### Bagian B: Segmentasi Warna

#### 6. Segmentasi Warna - K-Means Clustering

* **Konsep:** Ini adalah algoritma *unsupervised machine learning*. Tujuannya adalah untuk mengelompokkan semua piksel dalam gambar ke dalam `k` cluster (kelompok) berdasarkan warnanya.
* **Cara Kerja:**
    1.  **Reshape/Flatten:** Gambar (misal: 100x100x3) diubah bentuknya menjadi `(10000, 3)`. Setiap baris sekarang mewakili satu piksel dengan 3 nilai warnanya (R, G, B).
    2.  **Inisialisasi KMeans:** `KMeans(n_clusters=k)` memberi tahu algoritma untuk "menemukan `k` warna utama" dalam gambar. Di sini `k=4`.
    3.  **Training:** `kmeans.fit(pixel_values)` menjalankan algoritma. Ia akan menemukan 4 warna "pusat" (disebut **centroids**) yang paling mewakili semua piksel di gambar.
    4.  **Rekonstruksi Gambar:**
        * `kmeans.labels_`: Berisi label (0, 1, 2, atau 3) untuk setiap piksel, yang menunjukkan ke *centroid* mana piksel itu paling mirip.
        * `kmeans.cluster_centers_[...]`: Ini adalah langkah cerdas. Ini "mengganti" warna asli setiap piksel dengan warna *centroid* dari cluster tempat ia berada.
    5.  **Reshape Kembali:** Array `(10000, 3)` diubah kembali menjadi gambar `(100, 100, 3)` (ukuran asli). Hasilnya adalah gambar yang "posterized" (warnanya disederhanakan) menjadi hanya 4 warna.

#### 7. Segmentasi Warna - Thresholding HSV

* **Konsep:** Metode ini bertujuan untuk mengisolasi satu *rentang warna* tertentu (misalnya, semua yang berwarna hijau). Ini adalah metode berbasis *aturan* (rule-based).
* **Cara Kerja:**
    1.  **Konversi ke HSV:** `cv2.cvtColor(..., cv2.COLOR_RGB2HSV)` mengubah gambar ke ruang warna **HSV** (Hue, Saturation, Value).
    2.  **Mengapa HSV?** Ruang warna HSV jauh lebih baik untuk segmentasi warna. **Hue (H)** merepresentasikan warna itu sendiri (misalnya, merah, kuning, hijau), terlepas dari seberapa terang (`Value`) atau seberapa pekat (`Saturation`) warna itu. Ini jauh lebih mudah daripada mencoba mendefinisikan "hijau" dalam RGB.
    3.  **Tentukan Rentang:** `lower_hijau` dan `upper_hijau` mendefinisikan batas bawah dan atas dari rentang warna hijau yang ingin Anda deteksi.
    4.  **Buat Masker (Mask):** `cv2.inRange(...)` adalah fungsi kuncinya. Ia membuat gambar hitam-putih (biner) baru yang disebut *mask*. Piksel yang warnanya berada *di dalam* rentang (hijau) akan menjadi **putih**, dan yang di luar rentang akan menjadi **hitam**.
    5.  **Terapkan Masker:** `cv2.bitwise_and(...)` melakukan operasi AND logis. Ia "menjaga" piksel di gambar asli *hanya jika* piksel yang sesuai di masker berwarna putih. Hasilnya adalah gambar asli di mana semua yang *bukan* hijau telah dihitamkan.
