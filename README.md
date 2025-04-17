# Sürücüsüz Metro Simülasyonu (Rota Optimizasyonu)
<p> Bu proje, belirlenen metro istasyonları arasındaki en hızlı ve en az aktarmalı rotayı bulmayı amaçlamaktadır. BFS (Breadth-First Search) ve A* (A-Star) Algoritmalarını kullanarak rota hesaplamaları gerçekleştirilmiştir.</p>

## Kullanılan Teknolojiler ve Kütüphaneler

Proje Python ile geliştirilmiştir. Kullanılan kütüphaneler:

* `heapq`: A* algoritması için priority queue (öncelikli kuyruk) kullanımını sağlıyor.
* `collections`: BFS algoritması için queue (kuyruk) yönetimini sağlıyor.
* `typing`: Fonksiyonlarda tip belirtme (set,list,tuple vb.)
* `networkx`: Metro ağını grafik olarak modellemek ve görselleştirmek için kullanıldı.
* `matplotlib`: Metro ağını görselleştirmek için kullanıldı.

Projeyi çalıştırmak için: 
```
pip install networkx matplotlib
python GizemErol_MetroSimulation.py
```

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
3.  Komşular için g(n) ve f(n) = g(n) + h(n) değerleri hesaplanır.
4.  Hedefe ulaşıldığında, toplam süre ve en kısa rota döndürülür.

🔹 Başlangıç ve hedef istasyon kontrolü yapılır.
```
def en_hizli_rota_bul(self, baslangic_id: str, hedef_id: str) -> Optional[Tuple[List[Istasyon], int]]:
    if baslangic_id not in self.istasyonlar or hedef_id not in self.istasyonlar:
        return None
```
🔹 Heuristic fonksiyonu tanımlanır.
```
def heuristic(mevcut: Istasyon, hedef: Istasyon) -> int:
    return 5 if mevcut.hat != hedef.hat else 0
```
🔹 Öncelik kuyruğu (priority queue) oluşturuyoruz.
🔹 Maliyet sözlüğü ile her istasyon için şu ana kadar hesaplanan en kısa sürenin takibini yapıyoruz.
🔹 g_maliyet: Başlangıçtan bugüne kadar olan süre.
```
baslangic = self.istasyonlar[baslangic_id]
hedef = self.istasyonlar[hedef_id]
g_maliyet = {baslangic: 0}
pq = [(heuristic(baslangic, hedef), id(baslangic), baslangic, [baslangic])]
ziyaret_edildi = set()
```

🔹 Her döngüde, en düşük maliyetli istasyonu işleme alıyoruz.
🔹 Eğer istasyon hedefse, en hızlı rota ve toplam süre döndürülüyor.
```
while pq:
    f_degeri, _, mevcut, rota = heapq.heappop(pq)
    
    if mevcut == hedef:
        return rota, g_maliyet[mevcut] # Hedefe ulaşıldığında en kısa süre ve rota döndürülür.
```

🔹 Eğer istasyon daha önce ziyaret edilmişse, tekrar işlem yapmıyoruz.
```
if mevcut in ziyaret_edildi:
    continue
ziyaret_edildi.add(mevcut)
```

🔹 Komşu istasyonlar için yeni süre hesaplanıyor.
🔹 Eğer yeni süre önceki kayıttan daha düşükse, maliyet güncelleniyor(g(n) hesaplanır) ve f(n) değeri ile kuyruğa ekleniyor.
```
for komsu, sure in mevcut.komsular:
    yeni_g = g_maliyet[mevcut] + sure
    if komsu not in g_maliyet or yeni_g < g_maliyet[komsu]:
        g_maliyet[komsu] = yeni_g
        f_degeri = yeni_g + heuristic(komsu, hedef)
        heapq.heappush(pq, (f_degeri, id(komsu), komsu, rota + [komsu]))
```

## Neden A* Kullanıyoruz?

* Daha az düğüm gezerek hedefe ulaşma süresini optimize eder.
* Dijkstra'dan daha hızlıdır.

## Metro Ağının Görselleştirilmesi
<p> networkx ve matplotlib gibi kütüphaneler kullanılarak metro istasyonlarının bir grafik olarak çizilmesi sağlandı. Böylece kullanıcılar rotalarını görsel olarak takip edebilirler.</p>
 Grafikte:
🔹 İstasyonlar düğüm olarak gösterilir.
🔹 İstasyonlar arası bağlantılar çizgilerle gösterilir.
🔹 Farklı hatlar için örnek Kullanımda hatlar için belirtilen farklı renkler kullanılmıştır.
<li>[Güncelleme]: Daha önce görselleştirmede istasyonlar sahip oldukları id ile gösterilmişti, güncellemeden sonra her istasyonun ismi ile gösteriliyor.</li>

```
metro_gorsellestirme(metro)
```
![image](https://github.com/user-attachments/assets/6d1bcc60-81b6-4635-9c7d-872dba7a1a06)
* Görsel 1. Görselleştirme sonucu alınan çıktı.

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
Bu projeye ek olarak yapılabilir olan geliştirmeler:
<p>✔ 'Networkx' ve 'Matplotlib' gibi kütüphaneler kullanılarak oluşturulan metro ağı haritası daha detaylı hale getirilerek görselleştirilmesi geliştirilebilir.</p>
<p>✔ Tek bir en hızlı rota yerine, birkaç farklı rota sunarak yolcuların tercihlerine göre seçim yapmasına imkan tanınabilir (örneğin, en kısa süre, en az aktarma veya en az yürüyüş içeren rotalar).</p>
<p>✔ Makine öğrenmesi teknikleri kullanılarak, geçmiş metro hareketleri analiz edilip tahmini varış süreleri iyileştirilebilir ve algoritmaların doğruluğu artırılabilir.</p>
<p>✔ Kullanıcı dostu bir mobil uygulama entegrasyon sağlanarak, simülasyon gerçek zamanlı olarak daha etkileşimli bir hale getirilebilir.</p>

<p> Bu geliştirmeler, metro simülasyonunun günümüz koşullarını destekleyici, kullanıcı dostu ve gerçekçi bir sistem haline gelmesini sağlayabilir.</p>
