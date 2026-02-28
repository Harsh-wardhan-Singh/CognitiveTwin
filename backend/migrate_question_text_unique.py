"""
Migration script to fix the question_text unique constraint.
This removes the unique constraint to allow similar questions from LLM generation.
"""

from sqlalchemy import text, inspect
from app.db.session import engine

def remove_unique_constraint():
    """Remove unique constraint from question_text column"""
    
    print("Checking question_text constraint...")
    
    with engine.connect() as connection:
        try:
            # PostgreSQL: Drop the constraint
            connection.execute(text("""
                ALTER TABLE questions DROP CONSTRAINT questions_question_text_key;
            """))
            connection.commit()
            print("✓ Removed unique constraint from question_text")
            
        except Exception as e:
            # The constraint might not exist or database is different
            if "does not exist" in str(e):
                print("✓ Unique constraint doesn't exist (already removed)")
            elif "SQLite" in str(e) or "UNIQUE constraint" in str(e):
                # SQLite doesn't support ALTER TABLE DROP CONSTRAINT
                # But we can recreate the table without the constraint
                print("ℹ SQLite detected - constraint removal handled by model update")
            else:
                print(f"⚠ Could not remove constraint: {str(e)}")

if __name__ == "__main__":
    try:
        remove_unique_constraint()
    except Exception as e:
        print(f"Migration error: {str(e)}")
