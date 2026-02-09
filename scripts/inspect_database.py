# scripts/inspect_database.py
"""
Inspect existing PostgreSQL schema to generate SQLAlchemy models.
"""

import json

from sqlalchemy import create_engine, inspect


def inspect_database(database_url: str):
    """Analyze database schema and generate model templates."""
    engine = create_engine(database_url)
    inspector = inspect(engine)

    print("=" * 80)
    print("DATABASE SCHEMA ANALYSIS")
    print("=" * 80)

    tables = inspector.get_table_names()
    print(f"Found {len(tables)} tables:")

    schema_info = {}

    for table in tables:
        print(f"\n📊 Table: {table}")
        print("-" * 40)

        # Get columns
        columns = inspector.get_columns(table)
        print(f"Columns ({len(columns)}):")

        table_info = {
            "columns": [],
            "primary_key": [],
            "foreign_keys": [],
            "indexes": [],
        }

        for col in columns:
            col_info = {
                "name": col["name"],
                "type": str(col["type"]),
                "nullable": col.get("nullable", True),
                "default": col.get("default"),
                "autoincrement": col.get("autoincrement", False),
            }
            table_info["columns"].append(col_info)
            print(
                f"  - {col['name']}: {col['type']} "
                f"{'(PK)' if col.get('primary_key') else ''} "
                f"{'(nullable)' if col.get('nullable') else '(NOT NULL)'}"
            )

        # Get primary keys
        pk = inspector.get_pk_constraint(table)
        if pk["constrained_columns"]:
            table_info["primary_key"] = pk["constrained_columns"]
            print(f"Primary Key: {', '.join(pk['constrained_columns'])}")

        # Get foreign keys
        fks = inspector.get_foreign_keys(table)
        if fks:
            print("Foreign Keys:")
            for fk in fks:
                table_info["foreign_keys"].append(fk)
                print(
                    f"  - {fk['constrained_columns']} → "
                    f"{fk['referred_table']}.{fk['referred_columns']}"
                )

        schema_info[table] = table_info

    # Generate SQLAlchemy model templates
    print("\n" + "=" * 80)
    print("SQLALCHEMY MODEL TEMPLATES")
    print("=" * 80)

    for table_name, info in schema_info.items():
        generate_model_template(table_name, info)

    return schema_info


def generate_model_template(table_name: str, table_info: dict):
    """Generate SQLAlchemy model code from table info."""
    model_name = "".join(word.capitalize() for word in table_name.split("_"))

    print(f"\n# Model for table: {table_name}")
    print(f"class {model_name}(Base):")
    print(f'    """{model_name} model."""')
    print(f'    __tablename__ = "{table_name}"')
    print()

    # Generate columns
    for col in table_info["columns"]:
        col_name = col["name"]
        col_type = map_sql_type_to_sqlalchemy(col["type"])
        nullable = "True" if col["nullable"] else "False"

        # Handle primary key
        is_pk = col_name in table_info.get("primary_key", [])
        pk_str = ", primary_key=True" if is_pk else ""

        # Handle autoincrement
        auto_str = ", autoincrement=True" if col.get("autoincrement") else ""

        print(
            f"    {col_name} = Column({col_type}, nullable={nullable}{pk_str}{auto_str})"
        )

    # Generate relationships (simplified)
    for fk in table_info.get("foreign_keys", []):
        if fk["constrained_columns"]:
            col = fk["constrained_columns"][0]
            ref_table = fk["referred_table"]
            ref_model = "".join(word.capitalize() for word in ref_table.split("_"))

            print(f"\n    # Relationship to {ref_model}")
            print(f'    {col} = Column(String, ForeignKey("{ref_table}.id"))')
            print(
                f'    {ref_table.rstrip("s")} = relationship("{ref_model}", back_populates="{table_name}")'
            )

    print("\n    def __repr__(self):")
    print(f'        return f"<{model_name}(id={{self.id}})">')
    print()


def map_sql_type_to_sqlalchemy(sql_type: str) -> str:
    """Map SQL type to SQLAlchemy type."""
    type_map = {
        "integer": "Integer",
        "bigint": "BigInteger",
        "smallint": "SmallInteger",
        "serial": "Integer",
        "bigserial": "BigInteger",
        "varchar": "String",
        "text": "Text",
        "boolean": "Boolean",
        "timestamp": "DateTime",
        "date": "Date",
        "time": "Time",
        "numeric": "Numeric",
        "decimal": "Decimal",
        "float": "Float",
        "double precision": "Float",
        "json": "JSON",
        "jsonb": "JSONB",
        "uuid": "UUID",
    }

    sql_lower = sql_type.lower()
    for key, value in type_map.items():
        if key in sql_lower:
            return value

    return "String"  # Default


if __name__ == "__main__":
    # Use your database URL
    DATABASE_URL = "postgresql+psycopg2://postgres:aa@localhost:5434/premiumgym_bd"
    schema = inspect_database(DATABASE_URL)

    # Save schema info for reference
    with open("database_schema.json", "w") as f:
        json.dump(schema, f, indent=2, default=str)

    print("\n✅ Schema analysis complete. Check 'database_schema.json' for details.")
