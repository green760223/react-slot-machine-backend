import databases
import sqlalchemy

from config import config

metadata = sqlalchemy.MetaData()

employee_table = sqlalchemy.Table(
    "employee",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String),
    sqlalchemy.Column("department", sqlalchemy.String),
    sqlalchemy.Column("employee_id", sqlalchemy.String),
    sqlalchemy.Column("lottery_eligibility", sqlalchemy.String),
    sqlalchemy.Column("group", sqlalchemy.String),
    sqlalchemy.Column("prize", sqlalchemy.String),
    sqlalchemy.Column("is_won", sqlalchemy.Boolean, default=False, nullable=False),
    sqlalchemy.Column("is_donated", sqlalchemy.Boolean, default=False, nullable=False),
)

connect_args = {"check_same_thread": False} if "sqlite" in config.DATABASE_URL else {}
engine = sqlalchemy.create_engine(config.DATABASE_URL, connect_args=connect_args)

metadata.create_all(engine)

db_args = {"min_size": 5, "max_size": 30} if "postgres" in config.DATABASE_URL else {}
database = databases.Database(
    config.DATABASE_URL, force_rollback=config.DB_FORCE_ROLLBACK, **db_args
)
