from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
import random
import pandas as pd
import io
import time
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from database import engine, get_db, Base
import models
import schemas
from ai_agent import analyze_message_with_ai
Base.metadata.create_all(bind=engine)
app = FastAPI(
    title="Koopilot Backend API",
    description="KOBİ ve kooperatifler için AI destekli operasyon ajanı hackathon iskeleti",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rate Limiting State (In-Memory for Hackathon)
RATE_LIMIT_STORE = {}
RATE_LIMIT_SECONDS = 10
RATE_LIMIT_REQUESTS = 5

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"detail": "Sunucu tarafında beklenmeyen bir hata oluştu.", "error_msg": str(exc)}
    )

COMPANY_PROFILE = "Koopilot - Akıllı Operasyon ve Sipariş Yönetim Sistemi"
@app.get("/inventory", response_model=List[schemas.ProductResponse], summary="Mevcut ürünleri ve stok durumlarını listele")
def get_inventory(db: Session = Depends(get_db)):
    products = db.query(models.Product).all()
    return products
@app.put("/inventory/{product_id}", response_model=schemas.ProductResponse, summary="Ürün stok güncellemesi")
def update_inventory(product_id: int, stock: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Ürün bulunamadı")
    product.stock = stock
    db.commit()
    db.refresh(product)
    return product
@app.post("/inventory/upload", summary="Excel veya CSV dosyasından toplu ürün yükle")
async def upload_inventory(file: UploadFile = File(...), db: Session = Depends(get_db)):
    content = await file.read()
    
    # 1. Dosya Boyutu Sınırı (Max 5MB)
    if len(content) > 5 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="Dosya boyutu çok büyük. Maksimum 5MB yüklenebilir.")
        
    try:
        if file.filename.endswith('.xlsx'):
            df = pd.read_excel(io.BytesIO(content))
        elif file.filename.endswith('.csv'):
            df = pd.read_csv(io.BytesIO(content))
        else:
            raise HTTPException(status_code=400, detail="Sadece .xlsx veya .csv dosyaları desteklenmektedir.")
            
        # 2. Satır Sayısı Sınırı (Max 5000 Satır)
        if len(df) > 5000:
            raise HTTPException(status_code=400, detail="Dosya çok büyük. Maksimum 5000 satır yüklenebilir.")
        
        df.columns = [c.lower() for c in df.columns]
        required_cols = ['name', 'category', 'stock', 'price']
        for col in required_cols:
            if col not in df.columns:
                raise HTTPException(status_code=400, detail=f"Eksik sütun: {col}")
        updates = 0
        creations = 0
        for index, row in df.iterrows():
            try:
                stock_val = int(row['stock']) if pd.notna(row['stock']) else 0
                price_val = float(row['price']) if pd.notna(row['price']) else 0.0
                
                if stock_val < 0 or price_val < 0:
                    continue # Eksi değerleri atla veya hata fırlat. Şimdilik atlıyoruz.
                    
                product = db.query(models.Product).filter(models.Product.name == str(row['name'])).first()
                if product:
                    product.stock = stock_val
                    product.price = price_val
                    product.category = str(row['category'])
                    if 'unit' in df.columns and pd.notna(row['unit']): product.unit = str(row['unit'])
                    if 'description' in df.columns and pd.notna(row['description']): product.description = str(row['description'])
                    updates += 1
                else:
                    new_prod = models.Product(
                        name=str(row['name']),
                        category=str(row['category']),
                        stock=stock_val,
                        price=price_val,
                        unit=str(row.get('unit', 'Adet')) if pd.notna(row.get('unit')) else 'Adet',
                        description=str(row.get('description', '')) if pd.notna(row.get('description')) else ''
                    )
                    db.add(new_prod)
                    creations += 1
            except Exception as row_e:
                print(f"Satır {index} atlandı. Hata: {row_e}")
                continue
        db.commit()
        return {"status": "success", "updates": updates, "creations": creations}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Dosya işlenirken hata oluştu: {str(e)}")
@app.get("/orders", response_model=List[schemas.OrderResponse], summary="Tüm siparişleri listele")
def get_orders(db: Session = Depends(get_db)):
    orders = db.query(models.Order).all()
    return orders
@app.put("/orders/{order_id}/approve", response_model=schemas.OrderResponse, summary="Siparişi onayla ve stoktan düş")
def approve_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Sipariş bulunamadı")
    if order.status != models.OrderStatus.DRAFT:
        raise HTTPException(status_code=400, detail="Sadece 'Taslak' durumundaki siparişler onaylanabilir.")
    try:
        for item in order.items:
            product = db.query(models.Product).filter(models.Product.id == item.product_id).with_for_update().first()
            if not product:
                raise ValueError(f"Sipariş kalemi için ürün bulunamadı: {item.product_id}")
            if product.stock < item.quantity:
                raise ValueError(f"'{product.name}' ürünü için yetersiz stok! (Mevcut: {product.stock}, İstenen: {item.quantity})")
            product.stock -= item.quantity
        order.status = models.OrderStatus.APPROVED
        db.commit()
        db.refresh(order)
        return order
    except ValueError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Stok güncellenirken beklenmeyen bir hata oluştu.")
@app.get("/shipping/status/{order_id}", summary="Mock kargo durumu sorgulama")
def get_shipping_status(order_id: int, db: Session = Depends(get_db)):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Sipariş bulunamadı")
    if order.status == models.OrderStatus.DRAFT:
        return {"order_id": order_id, "shipping_status": "Henüz onaylanmadı"}
    statuses = ["Kargoya Verilmek Üzere Bekleniyor", "Kargoda - Yolda", "Teslim Edildi", "Transfer Merkezinde"]
    return {
        "order_id": order_id,
        "shipping_status": random.choice(statuses)
    }
@app.post("/ai/analyze-message", summary="Müşteri mesajını analiz et ve niyetine göre aksiyon al")
def analyze_message(request: schemas.MessageRequest, db: Session = Depends(get_db)):
    # 3. Rate Limiting Check (Simple In-Memory)
    client_id = request.session_id or "anonymous"
    current_time = time.time()
    
    if client_id not in RATE_LIMIT_STORE:
        RATE_LIMIT_STORE[client_id] = []
    
    # Eski istekleri temizle
    RATE_LIMIT_STORE[client_id] = [t for t in RATE_LIMIT_STORE[client_id] if current_time - t < RATE_LIMIT_SECONDS]
    
    if len(RATE_LIMIT_STORE[client_id]) >= RATE_LIMIT_REQUESTS:
        raise HTTPException(
            status_code=429, 
            detail=f"Çok fazla istek gönderdiniz. Lütfen {RATE_LIMIT_SECONDS} saniye bekleyin."
        )
        
    RATE_LIMIT_STORE[client_id].append(current_time)

    try:
        history_text = ""
        if request.session_id:
            past_logs = db.query(models.MessageLog).filter(
                models.MessageLog.session_id == request.session_id
            ).order_by(models.MessageLog.created_at.desc()).limit(5).all()
            
            if past_logs:
                past_logs.reverse()
                history_lines = []
                for log in past_logs:
                    history_lines.append(f"Müşteri: {log.raw_message}")
                    if log.ai_reply_draft:
                        history_lines.append(f"Ajan: {log.ai_reply_draft}")
                history_text = "\n".join(history_lines)

        all_products = db.query(models.Product).all()
        catalog_lines = []
        for p in all_products:
            catalog_lines.append(f"- {p.name} | Kategori: {p.category} | Fiyat: {p.price} TL | Stok: {p.stock} {p.unit}")
        catalog_text = "\n".join(catalog_lines)

        ai_result = analyze_message_with_ai(
            request.message, 
            company_profile=COMPANY_PROFILE,
            history=history_text,
            catalog=catalog_text
        )
        
        log_entry = models.MessageLog(
            session_id=request.session_id,
            raw_message=request.message,
            intent=ai_result.intent,
            ai_reply_draft=ai_result.ai_reply_draft
        )
        db.add(log_entry)
        db.commit()
        response_data = {
            "ai_analysis": ai_result.dict(),
            "created_order": None,
            "shipping_info": None,
            "warnings": []
        }
        if ai_result.intent == "new_order":
            existing_draft = None
            if request.session_id:
                existing_draft = db.query(models.Order).filter(
                    models.Order.session_id == request.session_id,
                    models.Order.status == models.OrderStatus.DRAFT
                ).first()

            if existing_draft:
                if ai_result.customer_name: existing_draft.customer_name = ai_result.customer_name
                if ai_result.phone: existing_draft.phone = ai_result.phone
                if ai_result.city: existing_draft.city = ai_result.city
                if ai_result.address: existing_draft.address = ai_result.address
                
                missing = []
                if not existing_draft.customer_name: missing.append("isim")
                if not existing_draft.phone: missing.append("telefon")
                if not existing_draft.address: missing.append("adres")
                existing_draft.missing_info = ", ".join(missing) if missing else None
                existing_draft.ai_reply_draft = ai_result.ai_reply_draft
                
                active_order = existing_draft
            else:
                new_order = models.Order(
                    session_id=request.session_id,
                    customer_name=ai_result.customer_name,
                    phone=ai_result.phone,
                    city=ai_result.city,
                    address=ai_result.address,
                    status=models.OrderStatus.DRAFT,
                    missing_info=", ".join(ai_result.missing_info) if ai_result.missing_info else None,
                    ai_reply_draft=ai_result.ai_reply_draft
                )
                db.add(new_order)
                db.flush()
                active_order = new_order

            warnings = []
            stock_info_list = []
            for ai_product in ai_result.products:
                matched_product = db.query(models.Product).filter(
                    models.Product.name.ilike(f"%{ai_product.name}%")
                ).first()
                if matched_product:
                    # Check if item already exists in this order to update qty, else create
                    existing_item = db.query(models.OrderItem).filter(
                        models.OrderItem.order_id == active_order.id,
                        models.OrderItem.product_id == matched_product.id
                    ).first()
                    
                    if existing_item:
                        # In a real app, you might add or replace. Here we replace.
                        existing_item.quantity = ai_product.quantity
                    else:
                        order_item = models.OrderItem(
                            order_id=active_order.id,
                            product_id=matched_product.id,
                            quantity=ai_product.quantity
                        )
                        db.add(order_item)
                        
                    stock_info_list.append(f"{matched_product.name} ({matched_product.stock} {matched_product.unit} mevcut)")
                else:
                    warnings.append(f"'{ai_product.name}' adlı ürün stokta bulunamadı.")
            db.commit()
            db.refresh(active_order)
            if stock_info_list:
                stock_note = " | ".join(stock_info_list)
                response_data["ai_analysis"]["ai_reply_draft"] += f"\n\n[Güncel Stok Bilgisi: {stock_note}]"
            response_data["created_order"] = {
                "order_id": active_order.id,
                "status": active_order.status,
                "missing_info": active_order.missing_info
            }
            response_data["warnings"] = warnings
        elif ai_result.intent == "shipping_query":
            search_query = None
            if ai_result.customer_name:
                search_query = models.Order.customer_name.ilike(f"%{ai_result.customer_name}%")
            elif ai_result.phone:
                search_query = models.Order.phone == ai_result.phone
            if search_query is not None:
                last_order = db.query(models.Order).filter(search_query).order_by(models.Order.order_date.desc()).first()
                if last_order:
                    status_info = get_shipping_status(last_order.id, db)
                    response_data["shipping_info"] = status_info
                    dynamic_reply = f"Merhaba {last_order.customer_name or 'Sayın Müşterimiz'}, " \
                                    f"siparişiniz (ID: {last_order.id}) şu anda şu durumda: **{status_info['shipping_status']}**."
                    response_data["ai_analysis"]["ai_reply_draft"] = dynamic_reply
                else:
                    response_data["warnings"].append("Müşteriye ait aktif bir sipariş bulunamadı.")
            else:
                response_data["warnings"].append("Kargo sorgusu için isim veya telefon bilgisi eksik.")
        return response_data
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Sistem Hatası: {str(e)}")