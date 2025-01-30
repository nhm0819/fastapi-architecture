import os
from typing import Any, List, Union

from sqlalchemy import Engine, create_engine, inspect, text
from sqlalchemy.schema import (
    DropConstraint,
    DropTable,
    ForeignKeyConstraint,
    MetaData,
    Table,
)

from alembic import command
from alembic.config import Config as AlembicConfig
from app.core.configs import config


class TestDbCoordinator:
    __test__ = True

    EXCLUDE_TABLES = {"alembic_version"}

    def apply_alembic(self) -> None:
        alembic_cfg = AlembicConfig("alembic.ini")
        command.ensure_version(alembic_cfg)
        # command.upgrade(alembic_cfg, "head")

    def truncate_all(self) -> None:
        url = config.WRITER_DB_URL.replace("aiomysql", "pymysql")
        engine = create_engine(url=url)
        tables, fkeys = self._get_all_tables_and_fkeys(engine=engine)
        for fkey in fkeys:
            with engine.begin() as conn:
                conn.execute(DropConstraint(fkey))
        for table in tables:
            with engine.begin() as conn:
                # conn.execute(DropTable(table))
                conn.execute(text(f"TRUNCATE TABLE {table.name}"))

    def _get_all_tables_and_fkeys(
        self, *, engine: Engine
    ) -> tuple[List[Table], List[Any]]:
        inspector = inspect(engine)
        meta = MetaData()
        tables = []
        all_fkeys = []

        for table_name in inspector.get_table_names():
            if table_name in self.EXCLUDE_TABLES:
                continue

            fkeys = []
            foreign_keys = inspector.get_foreign_keys(table_name)  # noqa: B023
            for fkey in foreign_keys:
                if not fkey["name"]:
                    continue
                fkeys.append(ForeignKeyConstraint((), (), name=fkey["name"]))
            tables.append(Table(table_name, meta, *fkeys))
            all_fkeys.extend(fkeys)

            # tables.append(table_name)

        return tables, all_fkeys
