"""Add classification tables

Revision ID: add_classification_tables
Revises: 001_initial
Create Date: 2024-03-09 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_classification_tables'
down_revision = '001_initial'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create classification_types table
    op.create_table(
        'classification_types',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('applies_to', sa.String(length=20), nullable=False),
        sa.Column('is_required', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_classification_types_id'), 'classification_types', ['id'], unique=False)
    op.create_index(op.f('ix_classification_types_name'), 'classification_types', ['name'], unique=False)

    # Create classification_values table
    op.create_table(
        'classification_values',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('classification_type_id', sa.Integer(), nullable=False),
        sa.Column('value', sa.String(length=100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('order', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['classification_type_id'], ['classification_types.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_classification_values_id'), 'classification_values', ['id'], unique=False)
    op.create_index(op.f('ix_classification_values_value'), 'classification_values', ['value'], unique=False)


def downgrade() -> None:
    # Drop classification_values table
    op.drop_index(op.f('ix_classification_values_value'), table_name='classification_values')
    op.drop_index(op.f('ix_classification_values_id'), table_name='classification_values')
    op.drop_table('classification_values')
    
    # Drop classification_types table
    op.drop_index(op.f('ix_classification_types_name'), table_name='classification_types')
    op.drop_index(op.f('ix_classification_types_id'), table_name='classification_types')
    op.drop_table('classification_types')
