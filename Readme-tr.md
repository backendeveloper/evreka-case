
## Target Case #1
Rest API servislerine yoğun bir şekilde konum, hız vb. lokasyon bilgisi alabilmelisiniz (bu verinin günde 1 milyon adet olduğunu düşünebilirsiniz). Bu verileri istediğiniz bir veritabanında saklayabilirsiniz. API servislerine gelen veriler asenkron olarak işlenmeli, bu nedenle bir kuyruk yönetim aracı kullanmanız gerekiyor, biz şu anda RabbitMQ veya Celery kullanıyoruz. Bu verilere belirli bir tarih aralığı için erişebilmeliyiz + şunları oluşturmalısınız Bir cihaz için yalnızca son verilere erişebildiğimiz Rest API hizmetleri.

## Target Case #2
TCP protokolü üzerinden konum, hız vb. lokasyon bilgilerini içeren verileri alabilmelisiniz (bu verilerden günde 1 milyon tane geldiğini hayal edebilirsiniz). Bu verileri istediğiniz bir veritabanında saklayabilirsiniz. Cihazlardan TCP sunucusuna gelen konum verileri asenkron olarak işlenmelidir çünkü bağlantının açık kalma süresi veri gönderen cihazların pil ömrünü olumsuz etkilemektedir. Biz şu anda RabbitMQ veya Celery kullanıyoruz. TCP sunucusuna gelen verileri belirli bir tarih aralığı + sadece bir cihaz için son verilere ulaşabileceğimiz Rest API servisleri hazırlamalısınız.
