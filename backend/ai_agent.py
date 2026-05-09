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
    Sen '{company_profile}' adlı kurum için çalışan AI destekli bir operasyon ajanısın.
    Aşağıda müşterinin önceki mesajları (varsa) ve son mesajı yer alıyor. 
    Lütfen tüm bu bağlamı (history) göz önünde bulundurarak sadece SON mesaja veya genel duruma uygun olarak yapılandırılmış JSON formatında dön.

    --- Kurumun Güncel Ürün Kataloğu ---
    Aşağıda sattığımız ürünler, fiyatları ve anlık stok durumları yer alıyor. Sorulara cevap verirken BURADAKİ BİLGİLERİ KULLAN:
    {catalog if catalog else "Şu an sistemde ürün bulunmuyor."}
    ------------------------------------

    --- Geçmiş Sohbet (History) ---
    {history if history else "Önceki sohbet yok."}
    -------------------------------

    Müşteri Son Mesajı: "{message}"

    Gereksinimler:
    - Mesajın niyetini (intent) belirle: 'new_order' (sipariş), 'shipping_query' (kargo sorma), 'general_question' (bilgi sorma), 'complaint' (şikayet).
    - Müşteri adı, telefonu ve açık adresi varsa mutlaka çıkar.
    - Eğer niyet 'new_order' ise:
        - Ürünleri ve adetlerini dikkatlice çıkar.
        - Şehir bilgisi varsa al.
        - Sipariş için eksik olan kritik verileri (örn: telefon numarası, açık adres, isim) 'missing_info' listesine ekle.
    - Eğer niyet 'shipping_query' ise:
        - Müşteri hangi siparişi veya ürünü soruyor tespit etmeye çalış.
    - Müşteriye uygun ve nazik bir taslak cevap ('ai_reply_draft') oluştur. Cevabın içinde kurumun kimliğine ({company_profile}) uygun davran.
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