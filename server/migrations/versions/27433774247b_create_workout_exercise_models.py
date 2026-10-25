"""Create workout exercise models

Revision ID: 27433774247b
Revises: 
Create Date: 2026-10-24 13:28:30.609903

"""
from alembic import op
import sqlalchemy as sa



revision = '27433774247b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('exercises',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('category', sa.String(length=50), nullable=False),
    sa.Column('equipment_needed', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('workouts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('duration_minutes', sa.Integer(), nullable=False),
    sa.Column('notes', sa.Text(), nullable=True),
    sa.CheckConstraint('duration_minutes > 0', name='check_workout_duration'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('workout_exercises',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('workout_id', sa.Integer(), nullable=False),
    sa.Column('exercise_id', sa.Integer(), nullable=False),
    sa.Column('reps', sa.Integer(), nullable=True),
    sa.Column('sets', sa.Integer(), nullable=True),
    sa.Column('duration_seconds', sa.Integer(), nullable=True),
    sa.CheckConstraint('duration_seconds IS NULL OR duration_seconds > 0', name='check_positive_seconds'),
    sa.CheckConstraint('reps IS NULL OR reps > 0', name='check_positive_reps'),
    sa.CheckConstraint('sets IS NULL OR sets > 0', name='check_positive_sets'),
    sa.ForeignKeyConstraint(['exercise_id'], ['exercises.id'], ),
    sa.ForeignKeyConstraint(['workout_id'], ['workouts.id'], ),
    sa.PrimaryKeyConstraint('id')
    )



def downgrade():
    op.drop_table('workout_exercises')
    op.drop_table('workouts')
    op.drop_table('exercises')
   
