"""Contents

Revision ID: 72770a5d61bb
Revises: 0cb715a5aac5
Create Date: 2022-11-05 19:27:30.315444

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "72770a5d61bb"
down_revision = "0cb715a5aac5"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "contents",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("parent_cr_id", sa.Integer(), nullable=False),
        sa.Column("data", sa.JSON(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["parent_cr_id"], ["cr.id"]),
    )
    op.create_table(
        "contents_pending",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("parent_cr_id", sa.Integer(), nullable=False),
        sa.Column("data", sa.JSON(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["parent_cr_id"], ["cr_pending.id"]),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("contents_pending")
    op.drop_table("contents")
    # ### end Alembic commands ###
