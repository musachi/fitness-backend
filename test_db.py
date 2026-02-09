import os
import sys

from sqlalchemy import text

from src.core.database import engine

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

try:
    # Probar conexión
    with engine.connect() as conn:
        result = conn.execute(text("SELECT version()"))
        db_version = result.scalar()
        print("✅ Conexión a PostgreSQL exitosa!")
        print(f"📊 Versión de PostgreSQL: {db_version}")

        # Verificar tablas existentes
        result = conn.execute(
            text(
                """
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
            ORDER BY table_name
        """
            )
        )
        tables = [row[0] for row in result]
        print(f"📋 Tablas en la base de datos ({len(tables)}):")
        for table in tables:
            print(f"  - {table}")

except Exception as e:
    print(f"❌ Error de conexión a la base de datos: {e}")
