"""Make exercises table completely dynamic

Revision ID: 001
Revises: previous_versions
Create Date: 2026-03-14 09:05:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    """Remove hardcoded classification columns from exercises table"""
    
    # Remove hardcoded classification columns
    op.drop_index('ix_exercises_movement_type_id', table_name='exercises')
    op.drop_index('ix_exercises_muscle_group_id', table_name='exercises')
    op.drop_index('ix_exercises_equipment_id', table_name='exercises')
    op.drop_index('ix_exercises_position_id', table_name='exercises')
    op.drop_index('ix_exercises_contraction_type_id', table_name='exercises')
    op.drop_index('ix_exercises_category_id', table_name='exercises')
    
    op.drop_column('movement_type_id', table_name='exercises')
    op.drop_column('muscle_group_id', table_name='exercises')
    op.drop_column('equipment_id', table_name='exercises')
    op.drop_column('position_id', table_name='exercises')
    op.drop_column('contraction_type_id', table_name='exercises')
    op.drop_column('category_id', table_name='exercises')


def downgrade():
    """Add back hardcoded classification columns"""
    
    # Add back hardcoded columns for rollback
    op.add_column('exercises', sa.Column('movement_type_id', sa.Integer(), nullable=True))
    op.add_column('exercises', sa.Column('muscle_group_id', sa.Integer(), nullable=True))
    op.add_column('exercises', sa.Column('equipment_id', sa.Integer(), nullable=True))
    op.add_column('exercises', sa.Column('position_id', sa.Integer(), nullable=True))
    op.add_column('exercises', sa.Column('contraction_type_id', sa.Integer(), nullable=True))
    op.add_column('exercises', sa.Column('category_id', sa.Integer(), nullable=True))
    
    # Recreate indexes
    op.create_index('ix_exercises_movement_type_id', 'exercises', ['movement_type_id'])
    op.create_index('ix_exercises_muscle_group_id', 'exercises', ['muscle_group_id'])
    op.create_index('ix_exercises_equipment_id', 'exercises', ['equipment_id'])
    op.create_index('ix_exercises_position_id', 'exercises', ['position_id'])
    op.create_index('ix_exercises_contraction_type_id', 'exercises', ['contraction_type_id'])
    op.create_index('ix_exercises_category_id', 'exercises', ['category_id'])
