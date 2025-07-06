from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class CompanyBase(BaseModel):
    symbol: str = Field(..., description="Symbol used for trading on the exchange")
    organ_code: str = Field(..., description="Unique identifier for the organization/company")
    isin_code: Optional[str] = Field(None, description="International Securities Identification Number")
    com_group_code: Optional[str] = Field(None, description="Company group classification code")
    icb_code: Optional[str] = Field(None, description="Industry Classification Benchmark code")
    organ_type_code: Optional[str] = Field(None, description="Organization type code")
    com_type_code: Optional[str] = Field(None, description="Company type code")
    organ_short_name: str = Field(..., description="Organization/company short name")
    organ_name: str = Field(..., description="Full name of the organization/company")
    business_descriptions: Optional[str] = Field(None, description="Description of main business activities")


class CompanyCreate(CompanyBase):
    pass


class CompanyUpdate(BaseModel):
    symbol: Optional[str] = None
    organ_code: Optional[str] = None
    isin_code: Optional[str] = None
    com_group_code: Optional[str] = None
    icb_code: Optional[str] = None
    organ_type_code: Optional[str] = None
    com_type_code: Optional[str] = None
    organ_short_name: Optional[str] = None
    organ_name: Optional[str] = None
    business_descriptions: Optional[str] = None


class CompanyInDBBase(CompanyBase):
    id: int
    create_date: Optional[datetime] = None
    update_date: Optional[datetime] = None

    class Config:
        from_attributes = True


class Company(CompanyInDBBase):
    pass 