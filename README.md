# Sürücüsüz Metro Simülasyonu (Rota Optimizasyonu)
<p> Bu proje, belirlenen metro istasyonları arasındaki en hızlı ve en az aktarmalı rotayı bulmayı amaçlamaktadır. BFS (Breadth-First Search) ve A* (A-Star) Algoritmalarını kullanarak rota hesaplamaları gerçekleştirilmiştir.</p>

## Kullanılan Teknolojiler ve Kütüphaneler

Proje Python ile geliştirilmiştir. Kullanılan kütüphaneler:

* `heapq`: A* algoritması için priority queue (öncelikli kuyruk) kullanımını sağlıyor.
* `collections`: BFS algoritması için queue (kuyruk) yönetimini sağlıyor.
* `typing`: Fonksiyonlarda tip belirtme (set,list,tuple vb.)

## Algoritmaların Çalışma Mantığı

1️⃣ BFS (Genişlik Öncelikli Arama) Algoritması

BFS, en kısa rotayı bulmak için düğümleri katman katman (level-wise) ziyaret eder. İlk olarak başlangıç istasyonunu kuyruk içine ekler ve her iterasyonda mevcut istasyonun komşularını sırayla ziyaret eder. 

BFS algoritması aşağıdaki durumda kullanışlıdır:

✔ En az aktarma yapılan rotayı bulmada etkilidir. (Çünkü BFS, kenar ağırlıklarını dikkate almaz ve en kısa düğüm derinliğini arar.)

**Çalışma Prensibi:**

1. Başlangıç istasyonu kuyruk içine eklenir.
2. Kuyruktan bir istasyon alınarak, komşu istasyonlar kuyruğa eklenir.
3. Hedef istasyona ulaşılana kadar tekrar edilir.

🔹 Başlangıç ve hedef istasyonların olup olmadığını kontrol ediyoruz. Eğer istasyonlardan biri eksikse None döndürülüyor.
```
def en_az_aktarma_bul(self, baslangic_id: str, hedef_id: str) -> Optional[List[Istasyon]]:
    if baslangic_id not in self.istasyonlar or hedef_id not in self.istasyonlar:
        return None
```
🔹 Kuyruk yapısını (deque) başlatıyoruz. İlk elemanımız başlangıç istasyonu ve onunla başlayan bir rota listesidir.
🔹 Ziyaret edilen istasyonları takip etmek için bir set oluşturuyoruz.

```
    baslangic = self.istasyonlar[baslangic_id]
    hedef = self.istasyonlar[hedef_id]
    ziyaret_edildi = {baslangic} 
    kuyruk = deque([(baslangic, [baslangic])])  # (mevcut istasyon, şu ana kadar olan rota)
```
🔹 Kuyruk dolu olduğu sürece, sıradaki istasyonu alıyoruz.
🔹 Eğer bu istasyon hedef istasyonsa, bulunan rota döndürülüyor.

```
    while kuyruk:
        mevcut, rota = kuyruk.popleft()
        
        if mevcut == hedef: 
            return rota  # Hedefe ulaşıldığında rota döndürülür.
```
🔹 Mevcut istasyonun komşularını kontrol ediyoruz.
🔹 Eğer bir komşu daha önce ziyaret edilmemişse, onu ziyaret edilmiş olarak işaretliyoruz ve kuyruğa ekliyoruz.

```
        for komsu, _ in mevcut.komsular:
            if komsu not in ziyaret_edildi:
                ziyaret_edildi.add(komsu)
                kuyruk.append((komsu, rota + [komsu]))  # Yeni rotayı oluşturup kuyruğa ekliyoruz.
```

2️⃣ A* (A-Star) Algoritması

A* algoritması, `gerçek maliyet (g) + tahmini maliyet (h) = toplam maliyet (f)` formülü ile çalışır.

* Gerçek maliyet (g): Şu ana kadar gidilen süre.
* Tahmini maliyet (h): İstasyonlar arasındaki indeks farkı.

A* algoritması aşağıdaki durumda kullanışlıdır:

✔ İki istasyon arasındaki en kısa sürede ulaşımı sağlamada etkilidir.

**Çalışma Prensibi:**

1.  Başlangıç istasyonu kuyruğa eklenir.
2.  Her iterasyonda, toplam maliyeti en düşük olan istasyon seçilir.
3.  Komşular hesaplanarak en iyi (en düşük f) olanlar kuyruğa eklenir.
4.  Hedefe ulaşıldığında, toplam süre ve en kısa rota döndürülür.

🔹 Başlangıç ve hedef istasyon kontrolü yapılır.
```
   def en_hizli_rota_bul(self, baslangic_id: str, hedef_id: str) -> Optional[Tuple[List[Istasyon], int]]:
    if baslangic_id not in self.istasyonlar or hedef_id not in self.istasyonlar:
        return None
```

🔹 Öncelik kuyruğu (priority queue) oluşturuyoruz.
🔹 Maliyet sözlüğü ile her istasyon için şu ana kadar hesaplanan en kısa sürenin takibini yapıyoruz.
```
    baslangic = self.istasyonlar[baslangic_id]
    hedef = self.istasyonlar[hedef_id]
    ziyaret_edildi = set()
    pq = [(0, id(baslangic), baslangic, [baslangic])]  # (toplam_sure, id(istasyon), istasyon, rota)
    maliyet = {baslangic: 0}
```

🔹 Her döngüde, en düşük maliyetli istasyonu işleme alıyoruz.
🔹 Eğer istasyon hedefse, en hızlı rota ve toplam süre döndürülüyor.
```
    while pq:
        toplam_sure, istasyon_id, mevcut, rota = heapq.heappop(pq)
        
        if mevcut == hedef:
            return rota, toplam_sure  # Hedefe ulaşıldığında en kısa süre ve rota döndürülür.
```

🔹 Eğer istasyon daha önce ziyaret edilmişse, tekrar işlem yapmıyoruz.
```
        if mevcut in ziyaret_edildi:
            continue
        ziyaret_edildi.add(mevcut)
```

🔹 Komşu istasyonlar için yeni süre hesaplanıyor.
🔹 Eğer yeni süre önceki kayıttan daha düşükse, maliyet güncelleniyor ve kuyruğa ekleniyor.
```
        for komsu, sure in mevcut.komsular:
            new_sure = toplam_sure + sure
            if komsu not in maliyet or new_sure < maliyet[komsu]:
                maliyet[komsu] = new_sure
                heapq.heappush(pq, (new_sure, id(komsu), komsu, rota + [komsu]))
```

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
## Projeyi Geliştirme Fikirleri:

