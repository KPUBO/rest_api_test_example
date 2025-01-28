"""database filling

Revision ID: 49d02b0cd743
Revises: 60f99d3b345f
Create Date: 2025-01-25 20:58:22.809448

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import geoalchemy2


# revision identifiers, used by Alembic.
revision: str = "49d02b0cd743"
down_revision: Union[str, None] = "60f99d3b345f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        INSERT INTO activities (id, parent_id, name, level) VALUES
        (1, NULL, 'Пищевая промышленность', 1),
        (2, 1, 'Мясная отрасль', 2),
        (3, 1, 'Молочная отрасль', 2),
        (4, 2, 'Мясо говядины', 3),
        (5, 2, 'Мясо свинины', 3),
        (6, 2, 'Мясо курицы', 3),
        (7, 3, 'Сыры', 3),
        (8, 3, 'Творог', 3),
        (9, NULL, 'Автомобильная промышленность', 1),
        (10, 9, 'Легковые автомобили', 2),
        (11, 9, 'Грузовые автомобили', 2),
        (12, 11, 'Запчасти', 3),
        (13, 11, 'Акссесуары', 3);
    """)
    op.execute("""
        INSERT INTO buildings (id, address, coords) VALUES
        (1, 'Пресненская набережная, 12', 'POINT(37.537932 55.749792)'),
        (2, 'ул. Лесная, 7', 'POINT(37.585870 55.776570)'),
        (3, 'Новинский бульвар, 8, стр. 1', 'POINT(37.583222 55.751244)'),
        (4, 'Смоленская площадь, 3', 'POINT(37.583600 55.747800)');
    """)
    op.execute("""
            INSERT INTO organizations (id, building_id, name) VALUES
            (1, 2, 'Молочная Линия'),
            (2, 4, 'Мясной Дом'),
            (3, 2, 'Деликатес-Мясо'),
            (4, 3, 'АромаПродукт'),
            (5, 1, 'Сливочный Дом'),
            (6, 1, 'Вектор Авто'),
            (7, 4, 'Горизонт Моторс'),
            (8, 2, 'Легенда Дорог'),
            (9, 1, 'СтримАвто');
            """)
    op.execute("""
                INSERT INTO phones (id, number, organization_id) VALUES
                (1, '+7 (495) 123-45-67', 5),
                (2, '+7 (499) 987-65-43', 5),
                (3, '+7 (812) 456-78-90', 5),
                (4, '+7 (341) 234-56-78', 6),
                (5, '+7 (383) 345-67-89', 6),
                (6, '+7 (351) 678-90-12', 6),
                (7, '+7 (473) 765-43-21', 4),
                (8, '+7 (343) 890-12-34', 3),
                (9, '+7 (831) 567-89-01', 7),
                (10, '+7 (401) 345-67-12', 7),
                (11, '+7 (499) 321-45-67', 7),
                (12, '+7 (495) 654-32-10', 3),
                (13, '+7 (812) 789-01-23', 7),
                (14, '+7 (346) 432-10-98', 2),
                (15, '+7 (421) 876-54-32', 8),
                (16, '+7 (861) 234-67-89', 1),
                (17, '+7 (423) 567-89-90', 8),
                (18, '+7 (473) 908-76-54', 9),
                (19, '+7 (343) 102-34-56', 8),
                (20, '+7 (341) 789-65-43', 1);
    """)

    op.execute("""
                    INSERT INTO organization_activity (organization_id, activity_id) VALUES
                    (4, 1),
                    (2, 2),
                    (1, 3),
                    (3, 4),
                    (5, 7),
                    (6, 9),
                    (7, 10),
                    (8, 13),
                    (9, 11),
                    (2, 3),
                    (5, 3);
    """)


def downgrade() -> None:
    op.execute("DELETE FROM activities WHERE id IN (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13);")
    op.execute("DELETE FROM buildings WHERE id IN (1, 2, 3, 4);")
    op.execute("DELETE FROM organizations WHERE id IN (1, 2, 3, 4, 5, 6, 7, 8, 9);")
    op.execute("DELETE FROM phones WHERE id IN (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20);")
    op.execute("DELETE FROM organization_activity WHERE organization_id IN (1, 2, 3, 4, 5, 6, 7, 8, 9);")