"""
Migration script to add has_taken_diagnostic column to users table.
Run this after updating the User model with the has_taken_diagnostic field.
"""

from sqlalchemy import text, inspect
from app.db.session import engine

def add_diagnostic_flag():
    """Add has_taken_diagnostic column to users table if it doesn't exist"""
    
    # Use inspector to check if column exists (works for all databases)
    inspector = inspect(engine)
    columns = [col['name'] for col in inspector.get_columns('users')]
    
    if 'has_taken_diagnostic' not in columns:
        print("Adding has_taken_diagnostic column to users table...")
        with engine.connect() as connection:
            try:
                # PostgreSQL syntax
                connection.execute(text("""
                    ALTER TABLE users ADD COLUMN has_taken_diagnostic BOOLEAN DEFAULT FALSE
                """))
                connection.commit()
                print("✓ Column added successfully to PostgreSQL database")
            except Exception as e:
                print(f"Error: {str(e)}")
                print("Could not add column to PostgreSQL")
                raise
    else:
        print("✓ has_taken_diagnostic column already exists")

if __name__ == "__main__":
    try:
        add_diagnostic_flag()
    except Exception as e:
        print(f"\nMigration failed: {str(e)}")

