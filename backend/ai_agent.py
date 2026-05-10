import os
from dotenv import load_dotenv
from google import genai
from schemas import AIFinalResponse
import json
def get_client():
    load_dotenv(override=True)
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or api_key == "your_gemini_api_key_here":
        return None
    return genai.Client(api_key=api_key)
def analyze_message_with_ai(message: str, company_profile: str = "Koopilot - KOBİ ve Kooperatif Operasyon Ajanı", history: str = "", catalog: str = "") -> AIFinalResponse:
    client = get_client()
    if not client:
        raise ValueError("Geçerli bir GEMINI_API_KEY bulunamadı. Lütfen .env dosyasını kontrol edin.")
    prompt = f"""
    Sen '{company_profile}' adlı kadın kooperatifleri ve KOBİ'ler için çalışan AI destekli bir operasyon ve sipariş yönetimi asistanısın.
    Amacın, müşterilerin doğal dille yazdığı mesajları anlamak ve kooperatif yöneticisinin işini kolaylaştıracak yapılandırılmış veriler üretmektir.

    --- KURUM KİMLİĞİ VE TON ---
    - Dilin nazik, yardımsever ve profesyonel olmalı (Kadın kooperatifi ruhuna uygun, samimi ama ciddi).
    - Müşterilere "Merhaba", "Değerli Müşterimiz", "🌿" gibi ifadelerle hitap edebilirsin.
    
    --- ÜRÜN KATALOĞU VE EŞLEŞTİRME ---
    Katalogdaki ürün isimleri ile müşterinin yazdığı isimler birebir tutmayabilir. 
    Örnek: "ev yapımı salça" -> "Domates Salçası" veya "acı biber" -> "Biber Salçası (Acı)" olabilir. 
    Lütfen en yakın anlamlı eşleşmeyi yapmaya çalış.
    
    Katalog:
    {catalog if catalog else "Şu an sistemde ürün bulunmuyor."}
    ------------------------------------

    --- GEÇMİŞ SOHBET (BAĞLAM) ---
    {history if history else "Önceki sohbet yok."}
    -------------------------------

    Müşteri Son Mesajı: "{message}"

    Gereksinimler:
    1. Mesajın niyetini (intent) belirle: 
       - 'new_order': Sipariş vermek istiyor.
       - 'shipping_query': "Kargom nerede?", "Ne zaman gelir?" gibi sorular.
       - 'complaint': "Ürün bozuk çıktı", "Geç geldi" gibi şikayetler.
       - 'return_request': "İade etmek istiyorum".
       - 'general_question': Ürün içeriği, fiyatı veya genel bilgi sorma.
    2. Eğer niyet 'new_order' ise:
       - Ürünleri, miktarlarını (quantity) ve birimlerini (unit) çıkar. 
       - Katalogdaki birimleri (kg, adet, kavanoz vb.) mutlaka kontrol et. 
       - Eğer müşteri miktar belirtmemişse, `quantity` alanını boş (null) bırak ve `missing_info` listesine mutlaka "miktar" veya hangi ürünün miktarı eksikse onu (örn: "çilek reçeli miktarı") ekle.
       - İsim, telefon, şehir ve açık adresi bulmaya çalış.
       - Eksik olan tüm bilgileri (isim, telefon, adres, miktar vb.) 'missing_info' listesine ekle.
    3. 'ai_reply_draft' alanına müşteriye gönderilecek cevabı yaz. 
       - Eğer bilgi eksikse (örn: adres yoksa veya miktar belirtilmemişse) nazikçe iste. 
       - Miktar isterken katalogdaki birimi kullan (Örn: "Kaç kavanoz çilek reçeli istersiniz?").
       - Eğer stokta olmayan bir ürün istenirse nazikçe belirt ve alternatif öner.
    """
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
        config={
            'response_mime_type': 'application/json',
            'response_schema': AIFinalResponse,
            'temperature': 0.1
        },
    )
    try:
        data = json.loads(response.text)
        return AIFinalResponse(**data)
    except Exception as e:
        error_msg = str(e)
        print(f"AI İşlem Hatası: {error_msg}")
        
        if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
            return AIFinalResponse(
                intent="general_question",
                ai_reply_draft="Sistemimizde anlık bir yoğunluk yaşanıyor. Lütfen yaklaşık 30-40 saniye bekleyip tekrar deneyiniz."
            )
            
        raise ValueError("Yapay zeka ile iletişim kurulurken bir hata oluştu.")