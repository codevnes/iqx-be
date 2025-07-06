from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, schemas
from app.api.v1 import deps

router = APIRouter()


@router.get("/", response_model=schemas.PaginatedResponse[schemas.Company])
async def read_companies(
    db: AsyncSession = Depends(deps.get_db),
    pagination: schemas.PaginationParams = Depends(deps.get_pagination_params),
) -> Any:
    """
    Retrieve companies with pagination and search.
    """
    companies, total = await crud.company.get_multi(
        db, skip=pagination.skip, limit=pagination.limit, search=pagination.search
    )
    return schemas.PaginatedResponse.create(items=companies, total=total, params=pagination)


@router.get("/symbol/{symbol}", response_model=schemas.Company)
async def read_company_by_symbol(
    *,
    db: AsyncSession = Depends(deps.get_db),
    symbol: str,
) -> Any:
    """
    Get company by symbol.
    """
    company = await crud.company.get_by_symbol(db, symbol=symbol)
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found",
        )
    return company


@router.post("/", response_model=schemas.Company)
async def create_company(
    *,
    db: AsyncSession = Depends(deps.get_db),
    company_in: schemas.CompanyCreate,
    current_user: schemas.User = Depends(deps.get_current_user),
) -> Any:
    """
    Create new company.
    """
    # Check if symbol already exists
    company_by_symbol = await crud.company.get_by_symbol(db, symbol=company_in.symbol)
    if company_by_symbol:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A company with this symbol already exists",
        )
    
    # Check if organ_code already exists
    company_by_organ_code = await crud.company.get_by_organ_code(db, organ_code=company_in.organ_code)
    if company_by_organ_code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A company with this organ_code already exists",
        )
    
    company = await crud.company.create(db, obj_in=company_in)
    return company


@router.get("/{company_id}", response_model=schemas.Company)
async def read_company(
    *,
    db: AsyncSession = Depends(deps.get_db),
    company_id: int,
) -> Any:
    """
    Get company by ID.
    """
    company = await crud.company.get(db, id=company_id)
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found",
        )
    return company


@router.put("/{company_id}", response_model=schemas.Company)
async def update_company(
    *,
    db: AsyncSession = Depends(deps.get_db),
    company_id: int,
    company_in: schemas.CompanyUpdate,
    current_user: schemas.User = Depends(deps.get_current_user),
) -> Any:
    """
    Update a company.
    """
    company = await crud.company.get(db, id=company_id)
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found",
        )
    
    # Check if symbol is being updated and is not unique
    if company_in.symbol and company_in.symbol != company.symbol:
        company_by_symbol = await crud.company.get_by_symbol(db, symbol=company_in.symbol)
        if company_by_symbol:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A company with this symbol already exists",
            )
    
    # Check if organ_code is being updated and is not unique
    if company_in.organ_code and company_in.organ_code != company.organ_code:
        company_by_organ_code = await crud.company.get_by_organ_code(db, organ_code=company_in.organ_code)
        if company_by_organ_code:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A company with this organ_code already exists",
            )
    
    company = await crud.company.update(db, db_obj=company, obj_in=company_in)
    return company


@router.delete("/{company_id}", response_model=schemas.Company)
async def delete_company(
    *,
    db: AsyncSession = Depends(deps.get_db),
    company_id: int,
    current_user: schemas.User = Depends(deps.get_current_user),
) -> Any:
    """
    Delete a company.
    """
    company = await crud.company.get(db, id=company_id)
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found",
        )
    company = await crud.company.delete(db, id=company_id)
    return company 