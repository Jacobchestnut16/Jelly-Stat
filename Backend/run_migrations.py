import os
import psycopg2

MIGRATIONS_DIR = "/app/db/migrations"

def get_db_url():
    url = os.getenv("DATABASE_URL")
    if not url:
        raise RuntimeError("DATABASE_URL is not set")
    return url

def ensure_migration_table(cur):
    cur.execute("""
CREATE TABLE IF NOT EXISTS schema_migrations (
id SERIAL PRIMARY KEY,
filename TEXT NOT NULL UNIQUE,
applied_at TIMESTAMP NOT NULL DEFAULT NOW()
);
    """)

def get_applied_migrations(cur):
    cur.execute("SELECT filename FROM schema_migrations;")
    return {row[0] for row in cur.fetchall()}

def apply_migration(cur, filename):
    path = os.path.join(MIGRATIONS_DIR, filename)
    print(f"Applying migration: {filename}")

    with open(path, "r", encoding="utf-8") as f:
        sql = f.read()

    cur.execute(sql)
    cur.execute(
        "INSERT INTO schema_migrations (filename) VALUES (%s)",
        (filename,)
    )
    print(f"Applied: {filename}")

def main():
    url = get_db_url()

    conn = psycopg2.connect(url)
    conn.autocommit = False
    cur = conn.cursor()

    ensure_migration_table(cur)
    applied = get_applied_migrations(cur)

    migrations = sorted(
        f for f in os.listdir(MIGRATIONS_DIR)
        if f.endswith(".sql")
    )

    new_migrations = [m for m in migrations if m not in applied]

    if not new_migrations:
        print("No new migrations.")
    else:
        print(f"Found {len(new_migrations)} new migration(s).")
        for m in new_migrations:
            apply_migration(cur, m)

    conn.commit()
    cur.close()
    conn.close()

    print("Migration complete.")

if __name__ == "__main__":
    main()
    