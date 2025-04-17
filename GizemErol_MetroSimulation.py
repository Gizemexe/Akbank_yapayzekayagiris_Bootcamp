from collections import defaultdict, deque
import heapq
from typing import Dict, List, Set, Tuple, Optional
import networkx as nx 
import matplotlib.pyplot as plt

class Istasyon:
    def __init__(self, idx: str, ad: str, hat: str):
        self.idx = idx
        self.ad = ad
        self.hat = hat
        self.komsular: List[Tuple['Istasyon', int]] = []  # (istasyon, süre) tuple'ları

    def komsu_ekle(self, istasyon: 'Istasyon', sure: int):
        self.komsular.append((istasyon, sure))

class MetroAgi:
    def __init__(self):
        self.istasyonlar: Dict[str, Istasyon] = {}
        self.hatlar: Dict[str, List[Istasyon]] = defaultdict(list)

    def istasyon_ekle(self, idx: str, ad: str, hat: str) -> None:
        if id not in self.istasyonlar:
            istasyon = Istasyon(idx, ad, hat)
            self.istasyonlar[idx] = istasyon
            self.hatlar[hat].append(istasyon)

    def baglanti_ekle(self, istasyon1_id: str, istasyon2_id: str, sure: int) -> None:
        istasyon1 = self.istasyonlar[istasyon1_id]
        istasyon2 = self.istasyonlar[istasyon2_id]
        istasyon1.komsu_ekle(istasyon2, sure)
        istasyon2.komsu_ekle(istasyon1, sure)
    
    def en_az_aktarma_bul(self, baslangic_id: str, hedef_id: str) -> Optional[List[Istasyon]]:
        if baslangic_id not in self.istasyonlar or hedef_id not in self.istasyonlar:
            return None
        
        baslangic = self.istasyonlar[baslangic_id]
        hedef = self.istasyonlar[hedef_id]
        ziyaret_edildi = {baslangic} 
        
        kuyruk = deque([(baslangic,[baslangic])]) # (mevcut istasyon , şuan ki rota)
        
        
        while kuyruk:
            mevcut, rota = kuyruk.popleft()
            
            if mevcut == hedef: 
                return rota # Hedefe ulaşınca mevcut rotayı döndür. 
            
            for komsu, _ in mevcut.komsular: # BFS search 
                if komsu not in ziyaret_edildi:
                    ziyaret_edildi.add(komsu)
                    kuyruk.append((komsu, rota + [komsu])) # rota + [komsu] = yeni rotayı mevcut rotaya ekleyerek devam.
                    
        return None 

    def en_hizli_rota_bul(self, baslangic_id: str, hedef_id: str) -> Optional[Tuple[List[Istasyon], int]]:
        if baslangic_id not in self.istasyonlar or hedef_id not in self.istasyonlar:
            return None
        
        def heuristic(mevcut: Istasyon, hedef: Istasyon) -> int:
            # Eğer istasyonlar aynı hatta değilse 5 dakika ceza ver
            return 5 if mevcut.hat != hedef.hat else 0
        
        baslangic = self.istasyonlar[baslangic_id]
        hedef = self.istasyonlar[hedef_id]    
        ziyaret_edildi = set()
        
        g_maliyet = {baslangic: 0}  # g(n): şu ana kadar olan maliyet
        pq = [(heuristic(baslangic, hedef), id(baslangic) ,baslangic, [baslangic])]
        
        while pq:
            f_degeri, _, mevcut,rota = heapq.heappop(pq)
            
            if mevcut == hedef:
                return rota, g_maliyet[mevcut]
            
            if mevcut in ziyaret_edildi:
                continue
            ziyaret_edildi.add(mevcut)
            
            for komsu, sure in mevcut.komsular: #A* algoritması 
                yeni_g  = g_maliyet[mevcut] + sure
                if komsu not in g_maliyet or yeni_g  < g_maliyet[komsu]: #En düşük süreye sahip rotayı seç
                    g_maliyet[komsu] = yeni_g 
                    f_degeri = yeni_g + heuristic(komsu, hedef)  # f(n) = g(n) + h(n)
                    heapq.heappush(pq,(f_degeri, id(komsu), komsu, rota + [komsu]))
        return None            
         
def metro_gorsellestirme(metro: MetroAgi):
    G = nx.Graph()

    # Düğüm ekleme
    for istasyon in metro.istasyonlar.values():
        G.add_node(istasyon.idx, label=istasyon.ad, color=istasyon.hat)

    hat_color = {
        "Kırmızı Hat": "red",
        "Mavi Hat": "blue",
        "Turuncu Hat": "orange"
    }

    # Kenarları ve süreleri ekle
    for istasyon in metro.istasyonlar.values():
        for komsu, sure in istasyon.komsular:
            if not G.has_edge(istasyon.idx, komsu.idx):
                G.add_edge(istasyon.idx, komsu.idx, weight=sure)

    renkler = [hat_color.get(G.nodes[n]["color"], "gray") for n in G.nodes]
    labels = {node: G.nodes[node]["label"] for node in G.nodes}
    edge_labels = nx.get_edge_attributes(G, 'weight')

    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(G, seed=42, k=0.3)  # Daha düzenli konumlandırma

    nx.draw_networkx_nodes(G, pos, node_color=renkler, node_size=2500)
    nx.draw_networkx_edges(G, pos, width=2.0, edge_color="gray")
    nx.draw_networkx_labels(G, pos, labels, font_size=10, font_color="white")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='black')

    plt.title("Metro Ağı Görselleştirme", fontsize=16)
    plt.axis('off')
    plt.tight_layout()
    plt.show()

# Örnek Kullanım
if __name__ == "__main__":
    metro = MetroAgi()
    
    # İstasyonlar ekleme
    # Kırmızı Hat
    metro.istasyon_ekle("K1", "Kızılay", "Kırmızı Hat")
    metro.istasyon_ekle("K2", "Ulus", "Kırmızı Hat")
    metro.istasyon_ekle("K3", "Demetevler", "Kırmızı Hat")
    metro.istasyon_ekle("K4", "OSB", "Kırmızı Hat")
    
    # Mavi Hat
    metro.istasyon_ekle("M1", "AŞTİ", "Mavi Hat")
    metro.istasyon_ekle("M2", "Kızılay", "Mavi Hat")  # Aktarma noktası
    metro.istasyon_ekle("M3", "Sıhhiye", "Mavi Hat")
    metro.istasyon_ekle("M4", "Gar", "Mavi Hat")
    
    # Turuncu Hat
    metro.istasyon_ekle("T1", "Batıkent", "Turuncu Hat")
    metro.istasyon_ekle("T2", "Demetevler", "Turuncu Hat")  # Aktarma noktası
    metro.istasyon_ekle("T3", "Gar", "Turuncu Hat")  # Aktarma noktası
    metro.istasyon_ekle("T4", "Keçiören", "Turuncu Hat")
    
    # Bağlantılar ekleme
    # Kırmızı Hat bağlantıları
    metro.baglanti_ekle("K1", "K2", 4)  # Kızılay -> Ulus
    metro.baglanti_ekle("K2", "K3", 6)  # Ulus -> Demetevler
    metro.baglanti_ekle("K3", "K4", 8)  # Demetevler -> OSB
    
    # Mavi Hat bağlantıları
    metro.baglanti_ekle("M1", "M2", 5)  # AŞTİ -> Kızılay
    metro.baglanti_ekle("M2", "M3", 3)  # Kızılay -> Sıhhiye
    metro.baglanti_ekle("M3", "M4", 4)  # Sıhhiye -> Gar
    
    # Turuncu Hat bağlantıları
    metro.baglanti_ekle("T1", "T2", 7)  # Batıkent -> Demetevler
    metro.baglanti_ekle("T2", "T3", 9)  # Demetevler -> Gar
    metro.baglanti_ekle("T3", "T4", 5)  # Gar -> Keçiören
    
    # Hat aktarma bağlantıları (aynı istasyon farklı hatlar)
    metro.baglanti_ekle("K1", "M2", 2)  # Kızılay aktarma
    metro.baglanti_ekle("K3", "T2", 3)  # Demetevler aktarma
    metro.baglanti_ekle("M4", "T3", 2)  # Gar aktarma
    
    # Test senaryoları
    print("\n=== Test Senaryoları ===")
    
    # Senaryo 1: AŞTİ'den OSB'ye
    print("\n1. AŞTİ'den OSB'ye:")
    rota = metro.en_az_aktarma_bul("M1", "K4")
    if rota:
        print("En az aktarmalı rota:", " -> ".join(i.ad for i in rota))
    
    sonuc = metro.en_hizli_rota_bul("M1", "K4")
    if sonuc:
        rota, sure = sonuc
        print(f"En hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota))
    
    # Senaryo 2: Batıkent'ten Keçiören'e
    print("\n2. Batıkent'ten Keçiören'e:")
    rota = metro.en_az_aktarma_bul("T1", "T4")
    if rota:
        print("En az aktarmalı rota:", " -> ".join(i.ad for i in rota))
    
    sonuc = metro.en_hizli_rota_bul("T1", "T4")
    if sonuc:
        rota, sure = sonuc
        print(f"En hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota))
    
    # Senaryo 3: Keçiören'den AŞTİ'ye
    print("\n3. Keçiören'den AŞTİ'ye:")
    rota = metro.en_az_aktarma_bul("T4", "M1")
    if rota:
        print("En az aktarmalı rota:", " -> ".join(i.ad for i in rota))
    
    sonuc = metro.en_hizli_rota_bul("T4", "M1")
    if sonuc:
        rota, sure = sonuc
        print(f"En hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota)) 
        
    metro_gorsellestirme(metro)    