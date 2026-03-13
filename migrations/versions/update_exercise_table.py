"""Update exercise table to match Excel template

Revision ID: update_exercise_table
Revises: add_classification_tables
Create Date: 2024-03-11 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'update_exercise_table'
down_revision = 'add_classification_tables'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add new column
    op.add_column('exercises', sa.Column('unit', sa.String(length=50), nullable=True))
    
    # Add is_active column if it doesn't exist
    op.add_column('exercises', sa.Column('is_active', sa.Boolean(), nullable=True, server_default='true'))
    
    # Drop columns that don't exist in Excel
    op.drop_index('ix_exercises_category_id', table_name='exercises')
    op.drop_column('exercises', 'category_id')
    
    op.drop_column('exercises', 'type')
    op.drop_column('exercises', 'crossfit_variant')


def downgrade() -> None:
    # Re-add dropped columns
    op.add_column('exercises', sa.Column('category_id', sa.Integer(), nullable=True))
    op.create_index('ix_exercises_category_id', 'exercises', ['category_id'], unique=False)
    
    op.add_column('exercises', sa.Column('type', sa.String(length=100), nullable=True))
    op.add_column('exercises', sa.Column('crossfit_variant', sa.JSON(), nullable=True))
    
    # Drop new columns
    op.drop_column('exercises', 'unit')
    op.drop_column('exercises', 'is_active')
