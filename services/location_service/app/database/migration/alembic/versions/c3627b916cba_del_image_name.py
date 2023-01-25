"""del image_name

Revision ID: c3627b916cba
Revises: 
Create Date: 2023-01-24 20:54:29.100616

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils



# revision identifiers, used by Alembic.
revision = 'c3627b916cba'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('locations',
    sa.Column('id', sa.Integer(), sa.Identity(always=False), nullable=False),
    sa.Column('location_uuid', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=False),
    sa.Column('user_uuid', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=False),
    sa.Column('location_name', sa.String(length=20), nullable=False),
    sa.Column('latitude', sa.Float(), nullable=True),
    sa.Column('longitude', sa.Float(), nullable=True),
    sa.Column('has_image', sa.Boolean(), nullable=False),
    sa.Column('description', sa.String(length=150), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_location_001', 'locations', ['user_uuid', 'location_name'], unique=True)
    op.create_index('idx_location_002', 'locations', ['user_uuid', 'location_uuid'], unique=True)
    op.create_index(op.f('ix_locations_location_name'), 'locations', ['location_name'], unique=False)
    op.create_index(op.f('ix_locations_location_uuid'), 'locations', ['location_uuid'], unique=False)
    op.create_index(op.f('ix_locations_user_uuid'), 'locations', ['user_uuid'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_locations_user_uuid'), table_name='locations')
    op.drop_index(op.f('ix_locations_location_uuid'), table_name='locations')
    op.drop_index(op.f('ix_locations_location_name'), table_name='locations')
    op.drop_index('idx_location_002', table_name='locations')
    op.drop_index('idx_location_001', table_name='locations')
    op.drop_table('locations')
    # ### end Alembic commands ###