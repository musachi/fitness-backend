"""Add exercise dynamic fields

Revision ID: add_exercise_dynamic_fields
Revises: add_plan_description_goal_level
Create Date: 2026-03-12 09:08:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_exercise_dynamic_fields'
down_revision = 'add_plan_fields'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add missing columns to exercises table
    op.add_column('exercises', sa.Column('is_active', sa.Boolean(), nullable=True, default=True))
    
    # Create exercise_classifications table
    op.create_table('exercise_classifications',
        sa.Column('exercise_id', sa.Integer(), nullable=False),
        sa.Column('classification_value_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['classification_value_id'], ['classification_values.id'], ),
        sa.ForeignKeyConstraint(['exercise_id'], ['exercises.id'], ),
        sa.PrimaryKeyConstraint('exercise_id', 'classification_value_id')
    )


def downgrade() -> None:
    # Remove exercise_classifications table
    op.drop_table('exercise_classifications')
    
    # Remove is_active column
    op.drop_column('exercises', 'is_active')
