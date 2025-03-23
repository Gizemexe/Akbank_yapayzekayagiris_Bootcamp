# Sürücüsüz Metro Simülasyonu (Rota Optimizasyonu)
<p> Bu proje, belirlenen metro istasyonları arasındaki en hızlı ve en az aktarmalı rotayı bulmayı amaçlamaktadır. BFS (Breadth-First Search) ve A* (A-Star) Algoritmalarını kullanarak rota hesaplamaları gerçekleştirilmiştir.</p>

## Kullanılan Teknolojiler ve Kütüphaneler

Proje Python ile geliştirilmiştir. Kullanılan kütüphaneler:

* `heapq`: A* algoritması için öncelikli kuyruk (priority queue)
* `collections`: BFS algoritması için kuyruk (queue) yönetimi
* `typing`: Fonksiyonlarda tip belirtimleri

## Algoritmaların Çalışma Mantığı

1️⃣ BFS (Genişlik Öncelikli Arama) Algoritması

BFS, en kısa rotayı bulmak için düğümleri katman katman (level-wise) ziyaret eder. İlk olarak başlangıç istasyonunu kuyruk içine ekler ve her iterasyonda mevcut istasyonun komşularını sırayla ziyaret eder. BFS algoritması aşağıdaki durumlarda kullanışlıdır:

✔ En az aktarma yapılan rotayı bulmada etkilidir. (Çünkü BFS, kenar ağırlıklarını dikkate almaz ve en kısa düğüm derinliğini arar.)

**Çalışma Prensibi:**

1.  Başlangıç istasyonu kuyruğa eklenir.
2.  Kuyruktan bir istasyon alınır ve komşu istasyonlar kuyruğa eklenir.
3.  Hedef istasyona ulaşılana kadar tekrar edilir.

2️⃣ A* (A-Star) Algoritması

A* algoritması, `gerçek maliyet (g) + tahmini maliyet (h) = toplam maliyet (f)` formülü ile çalışır.

* Gerçek maliyet (g): Şu ana kadar gidilen süre.
* Tahmini maliyet (h): İstasyonlar arasındaki indeks farkı.

**Çalışma Prensibi:**

1.  Başlangıç istasyonu kuyruğa eklenir.
2.  Her iterasyonda, toplam maliyeti en düşük olan istasyon seçilir.
3.  Komşular hesaplanarak en iyi (en düşük f) olanlar kuyruğa eklenir.
4.  Hedefe ulaşıldığında, toplam süre ve en kısa rota döndürülür.
   
**Avantajları:**

* Hedefe ulaşma süresini optimize eder.
* Dijkstra'dan daha hızlıdır.

## Neden A* Kullanıyoruz?

* Daha az düğüm gezerek hedefe ulaşma süresini optimize eder.
* Dijkstra'dan daha hızlıdır.

## Örnek Kullanım ve Test Sonuçları

### Kod örneği:

```
metro = MetroAgi()
metro.en_az_aktarma_bul("M1", "K4")
metro.en_hizli_rota_bul("M1", "K4")
```
### Örnek Çıktı:
```
En az aktarmalı rota: AŞTİ -> Kızılay -> Kızılay -> Ulus -> Demetevler -> OSB
En hızlı rota (25 dakika): AŞTİ -> Kızılay -> Kızılay -> Ulus -> Demetevler -> OSB
```
