"""create_companies_table

Revision ID: 21fe6fecd971
Revises: f4444f5dfbe4
Create Date: 2025-07-07 01:36:27.111222

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '21fe6fecd971'
down_revision: Union[str, Sequence[str], None] = 'f4444f5dfbe4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'companies',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('symbol', sa.String(20), index=True, unique=True, nullable=False),
        sa.Column('organ_code', sa.String(50), index=True, unique=True, nullable=False),
        sa.Column('isin_code', sa.String(50), index=True, unique=True, nullable=True),
        sa.Column('com_group_code', sa.String(50), index=True, nullable=True),
        sa.Column('icb_code', sa.String(50), index=True, nullable=True),
        sa.Column('organ_type_code', sa.String(50), index=True, nullable=True),
        sa.Column('com_type_code', sa.String(50), index=True, nullable=True),
        sa.Column('organ_short_name', sa.String(100), index=True, nullable=False),
        sa.Column('organ_name', sa.String(255), index=True, nullable=False),
        sa.Column('business_descriptions', sa.Text(), nullable=True),
        sa.Column('create_date', sa.DateTime(), default=sa.func.now()),
        sa.Column('update_date', sa.DateTime(), default=sa.func.now(), onupdate=sa.func.now()),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('companies')
