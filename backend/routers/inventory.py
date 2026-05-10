from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import pandas as pd
import io
from database import get_db
import models
import schemas

router = APIRouter(
    prefix="/inventory",
    tags=["Inventory"]
)

@router.get("", response_model=List[schemas.ProductResponse], summary="Mevcut ürünleri ve stok durumlarını listele")
def get_inventory(db: Session = Depends(get_db)):
    products = db.query(models.Product).all()
    return products

@router.get("/alerts", response_model=List[schemas.ProductResponse], summary="Stok seviyesi düşük ( < 5) olan ürünleri listele")
def get_inventory_alerts(db: Session = Depends(get_db)):
    products = db.query(models.Product).filter(models.Product.stock < 5).all()
    return products

@router.post("", response_model=schemas.ProductResponse, summary="Yeni ürün ekle")
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    db_product = models.Product(
        name=product.name,
        description=product.description,
        category=product.category,
        unit=product.unit,
        stock=product.stock,
        price=product.price
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@router.put("/{product_id}", response_model=schemas.ProductResponse, summary="Ürün bilgilerini güncelle")
def update_product(product_id: int, update_data: schemas.ProductCreate, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Ürün bulunamadı")
    
    product.name = update_data.name
    product.description = update_data.description
    product.category = update_data.category
    product.unit = update_data.unit
    product.stock = update_data.stock
    product.price = update_data.price
    
    db.commit()
    db.refresh(product)
    return product

@router.post("/upload", summary="Excel veya CSV dosyasından toplu ürün yükle")
async def upload_inventory(file: UploadFile = File(...), db: Session = Depends(get_db)):
    content = await file.read()
    
    if len(content) > 5 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="Dosya boyutu çok büyük. Maksimum 5MB yüklenebilir.")
        
    try:
        if file.filename.endswith('.xlsx'):
            df = pd.read_excel(io.BytesIO(content))
        elif file.filename.endswith('.csv'):
            df = pd.read_csv(io.BytesIO(content))
        else:
            raise HTTPException(status_code=400, detail="Sadece .xlsx veya .csv dosyaları desteklenmektedir.")
            
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
                # Float conversion for flexibility (kg, liters etc)
                stock_val = float(row['stock']) if pd.notna(row['stock']) else 0.0
                price_val = float(row['price']) if pd.notna(row['price']) else 0.0
                
                if stock_val < 0 or price_val < 0:
                    continue
                    
                # Use name to find existing product
                product_name = str(row['name']).strip()
                product = db.query(models.Product).filter(models.Product.name == product_name).first()
                
                if product:
                    product.stock = stock_val
                    product.price = price_val
                    product.category = str(row['category']).strip()
                    if 'unit' in df.columns and pd.notna(row['unit']): 
                        product.unit = str(row['unit']).strip()
                    if 'description' in df.columns and pd.notna(row['description']): 
                        product.description = str(row['description']).strip()
                    updates += 1
                else:
                    new_prod = models.Product(
                        name=product_name,
                        category=str(row['category']).strip(),
                        stock=stock_val,
                        price=price_val,
                        unit=str(row.get('unit', 'Adet')).strip() if pd.notna(row.get('unit')) else 'Adet',
                        description=str(row.get('description', '')).strip() if pd.notna(row.get('description')) else ''
                    )
                    db.add(new_prod)
                    creations += 1
            except Exception as e:
                print(f"Row {index} processing error: {e}")
                continue
        db.commit()
        return {"status": "success", "updates": updates, "creations": creations}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Dosya işlenirken hata oluştu: {str(e)}")