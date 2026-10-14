
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import get_db
from models import Material

router = APIRouter(
    prefix="/api/v1/materials",
    tags=["Materials"]
)


class MaterialCreate(BaseModel):
    name: str = Field(min_length=2)
    price_per_kg: float = Field(gt=0)
    stock_kg: float = Field(ge=0)


class StockUpdate(BaseModel):
    stock_kg: float = Field(ge=0)


def material_to_dict(material: Material):
    return {
        "id": material.id,
        "name": material.name,
        "price_per_kg": material.price_per_kg,
        "stock_kg": material.stock_kg
    }


@router.get("/")
def get_materials(
    min_stock: float | None = None,
    db: Session = Depends(get_db)
):
    query = select(Material)

    if min_stock is not None:
        query = query.where(Material.stock_kg >= min_stock)

    result = db.scalars(query).all()

    return [material_to_dict(m) for m in result]

@router.get("/summary")
def inventory_summary(db: Session = Depends(get_db)):
    all_materials = db.scalars(select(Material)).all()

    total_value = sum(
        material.price_per_kg * material.stock_kg
        for material in all_materials
    )

    return {
        "total_materials": len(all_materials),
        "total_inventory_value": round(total_value, 2)
    }

@router.get("/{material_id}")
def get_material(
    material_id: int,
    db: Session = Depends(get_db)
):
    material = db.get(Material, material_id)

    if material is None:
        raise HTTPException(
            status_code=404,
            detail="Material not found"
        )

    return material_to_dict(material)


@router.post("/", status_code=201)
def create_material(
    data: MaterialCreate,
    db: Session = Depends(get_db)
):
    new_material = Material(**data.model_dump())

    db.add(new_material)
    db.commit()
    db.refresh(new_material)

    return material_to_dict(new_material)


@router.patch("/{material_id}/stock")
def update_stock(
    material_id: int,
    data: StockUpdate,
    db: Session = Depends(get_db)
):
    material = db.get(Material, material_id)

    if material is None:
        raise HTTPException(
            status_code=404,
            detail="Material not found"
        )

    material.stock_kg = data.stock_kg

    db.commit()
    db.refresh(material)

    return material_to_dict(material)


@router.put("/{material_id}")
def update_material(
    material_id: int,
    data: MaterialCreate,
    db: Session = Depends(get_db)
):
    material = db.get(Material, material_id)

    if material is None:
        raise HTTPException(
            status_code=404,
            detail="Material not found"
        )

    material.name = data.name
    material.price_per_kg = data.price_per_kg
    material.stock_kg = data.stock_kg

    db.commit()
    db.refresh(material)

    return material_to_dict(material)


@router.delete("/{material_id}")
def delete_material(
    material_id: int,
    db: Session = Depends(get_db)
):
    material = db.get(Material, material_id)

    if material is None:
        raise HTTPException(
            status_code=404,
            detail="Material not found"
        )

    db.delete(material)
    db.commit()

    return {
        "message": "Material deleted successfully"
    }

