""
	Database ismi db_1,db_2,db_3,db_4 olmalı
""
1)getlinks.py dosyası istenen bir şehirden linkleri toplar
2)checklinks.py dosyası her restaurantın menüsü kontrol edip verileri indiriyor
3)getInfo.py çıkarılan objelerden bilgi çıkarıp veri için ortak bir txt
dosyası oluşturuyor
4)construct_database.py veri tabanını kuruyor
5)match_database.py veri tabanındaki yorumlar ile menüleri eşleştiriyor
6)getdataset.py verilen parametreler ile veri seti çekiyor
Formatı:python city location restaurant_name speed service flavour
örnek kod:python getdataset.py ankara n n 9 9 9
çıktı olarak csv dosyaları oluşturuluyor
7)statistical_analysis.py
Yorumlar ve menüler üzerinde bazı analizler yapıyor
Örnek:
python statistical_analysis.py ankara bilkent-merkez-kampüs burger-king
8)clustering.py 
Restaurantları servis,hız ve lezzet durumuna göre kümeliyor.
python clustering.py