from typing import Any, Dict, List, Optional, Union, Tuple

from sqlalchemy import or_, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.company import Company
from app.schemas.company import CompanyCreate, CompanyUpdate


class CRUDCompany:
    async def get(self, db: AsyncSession, *, id: int) -> Optional[Company]:
        result = await db.execute(select(Company).filter(Company.id == id))
        return result.scalars().first()

    async def get_by_symbol(self, db: AsyncSession, *, symbol: str) -> Optional[Company]:
        result = await db.execute(select(Company).filter(Company.symbol == symbol))
        return result.scalars().first()
    
    async def get_by_organ_code(self, db: AsyncSession, *, organ_code: str) -> Optional[Company]:
        result = await db.execute(select(Company).filter(Company.organ_code == organ_code))
        return result.scalars().first()

    async def get_multi(
        self, db: AsyncSession, *, skip: int = 0, limit: int = 100, search: Optional[str] = None
    ) -> Tuple[List[Company], int]:
        query = select(Company)
        
        # Apply search filter if provided
        if search:
            search_term = f"%{search}%"
            query = query.filter(
                or_(
                    Company.symbol.ilike(search_term),
                    Company.organ_code.ilike(search_term),
                    Company.organ_short_name.ilike(search_term),
                    Company.organ_name.ilike(search_term)
                )
            )
        
        # Get total count
        count_query = select(func.count()).select_from(query.subquery())
        total = await db.execute(count_query)
        total_count = total.scalar()
        
        # Apply pagination
        query = query.offset(skip).limit(limit)
        
        # Execute query
        result = await db.execute(query)
        return result.scalars().all(), total_count

    async def create(self, db: AsyncSession, *, obj_in: CompanyCreate) -> Company:
        db_obj = Company(**obj_in.model_dump())
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(
        self, db: AsyncSession, *, db_obj: Company, obj_in: Union[CompanyUpdate, Dict[str, Any]]
    ) -> Company:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def delete(self, db: AsyncSession, *, id: int) -> Optional[Company]:
        company = await self.get(db, id=id)
        if company:
            await db.delete(company)
            await db.commit()
        return company


company = CRUDCompany() 