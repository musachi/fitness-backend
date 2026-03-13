"""Create dynamic exercise classification system

Revision ID: create_dynamic_exercise_system
Revises: update_exercise_table
Create Date: 2024-03-12 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'create_dynamic_exercise_system'
down_revision = 'update_exercise_table'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create the intermediate table for exercise-classification relationships
    op.create_table(
        'exercise_classifications',
        sa.Column('exercise_id', sa.Integer(), nullable=False),
        sa.Column('classification_value_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=True),
        sa.ForeignKeyConstraint(['classification_value_id'], ['classification_values.id'], ),
        sa.ForeignKeyConstraint(['exercise_id'], ['exercises.id'], ),
        sa.PrimaryKeyConstraint('exercise_id', 'classification_value_id')
    )
    
    # Create indexes for better performance
    op.create_index('ix_exercise_classifications_exercise_id', 'exercise_classifications', ['exercise_id'])
    op.create_index('ix_exercise_classifications_classification_value_id', 'exercise_classifications', ['classification_value_id'])


def downgrade() -> None:
    # Drop indexes
    op.drop_index('ix_exercise_classifications_classification_value_id', table_name='exercise_classifications')
    op.drop_index('ix_exercise_classifications_exercise_id', table_name='exercise_classifications')
    
    # Drop the intermediate table
    op.drop_table('exercise_classifications')
