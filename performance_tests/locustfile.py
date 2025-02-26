from locust import HttpUser, task, between

class EStoreUser(HttpUser):
    # Kullanıcılar arasında 1-3 saniye bekleme süresi
    wait_time = between(1, 3)

    @task(1)
    def view_products(self):
        """
        Ürünlerin listelendiği API'ye istek gönderir.
        """
        self.client.get("/products")

    @task(2)
    def view_product_detail(self):
        """
        Örneğin ID'si 1 olan ürünün detayını görüntüler.
        Gerçek uygulamada dinamik ID'ler kullanılabilir.
        """
        product_id = 1  # Dinamik hale getirilebilir
        self.client.get(f"/products/{product_id}")

    @task(1)
    def add_to_cart(self):
        """
        Ürünü sepete ekleme işlemini simüle eder.
        """
        payload = {"product_id": 1, "quantity": 1}
        self.client.post("/cart/add", json=payload)

    @task(1)
    def checkout(self):
        """
        Sepetteki ürünlerin satın alma işlemini gerçekleştirir.
        """
        payload = {"payment_method": "credit_card", "address_id": 1}
        self.client.post("/checkout", json=payload)