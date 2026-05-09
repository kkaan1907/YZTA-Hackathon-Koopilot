from database import SessionLocal, engine, Base
import models
from datetime import datetime, timedelta
def init_db():
    print("Veritabanı tabloları oluşturuluyor...")
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        if db.query(models.Product).first():
            print("Veritabanında zaten veriler mevcut. İşlem atlanıyor.")
            return
        print("Dummy ürünler ekleniyor...")
        products = [
            models.Product(name="Ev Yapımı Domates Salçası 1Kg", category="Gıda", stock=50, price=120.0),
            models.Product(name="Hakiki Nar Ekşisi 500ml", category="Gıda", stock=30, price=150.0),
            models.Product(name="Keten Kumaş Masa Örtüsü", category="Tekstil", stock=15, price=300.0),
            models.Product(name="Organik Sızma Zeytinyağı 1L", category="Gıda", stock=20, price=350.0),
            models.Product(name="El Dokuması Kilim", category="Ev Dekorasyonu", stock=5, price=1200.0)
        ]
        db.add_all(products)
        db.commit()
        print("Geçmiş siparişler ekleniyor...")
        order1 = models.Order(
            customer_name="Ayşe Yılmaz",
            phone="05551234567",
            city="İstanbul",
            status=models.OrderStatus.APPROVED,
            order_date=datetime.utcnow() - timedelta(days=2)
        )
        order2 = models.Order(
            customer_name="Mehmet Demir",
            phone="05329876543",
            city="Ankara",
            status=models.OrderStatus.SHIPPED,
            order_date=datetime.utcnow() - timedelta(days=5)
        )
        db.add_all([order1, order2])
        db.commit()
        item1 = models.OrderItem(order_id=order1.id, product_id=products[0].id, quantity=2)
        item2 = models.OrderItem(order_id=order1.id, product_id=products[1].id, quantity=1)
        item3 = models.OrderItem(order_id=order2.id, product_id=products[2].id, quantity=1)
        db.add_all([item1, item2, item3])
        db.commit()
        print("Başlangıç verileri başarıyla eklendi!")
    except Exception as e:
        print(f"Veri eklerken hata oluştu: {e}")
        db.rollback()
    finally:
        db.close()
if __name__ == "__main__":
    init_db()