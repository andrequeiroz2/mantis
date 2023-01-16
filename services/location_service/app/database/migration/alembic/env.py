from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from database.migration.helper import DBSchemaMigrate
from alembic import context
from core.config import settings
from database.base import Base
from database.model.location import LocationModel


target_metadata = Base.metadata

# Configura contexto do migration
# context.config.set_main_option(
#     "sqlalchemy.url",
#     f"postgresql+psycopg2://{settings.DBUSER}:{settings.DBPASSWORD}@{settings.DBHOST}:{settings.DBPORT}/{settings.DBBASE}"
# )

context.config.set_main_option("sqlalchemy.url", settings.SQLALCHEMY_DATABASE_STR)

alembic_config = context.config
fileConfig(alembic_config.config_file_name)


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    engine = engine_from_config(
        alembic_config.get_section(alembic_config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with engine.connect() as connection:

        # DBSM = DBSchemaMigrate(connection)
        # DBSM.init_db()

        url = context.config.get_main_option("sqlalchemy.url")
        context.configure(
            url=url,
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
        )

        with context.begin_transaction():
            context.run_migrations()


def run_migrations_offline():
    """Como utilizamos muitas customizacoes do alembic para atender ao Multi Tennant,
    nao eh possivel rodar em modo offline
    """
    return


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

