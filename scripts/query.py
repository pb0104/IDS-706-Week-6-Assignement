import sqlite3
import os

def main():
    # Path to the DB (adjust if needed)
    db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'university_database.db')
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    print("=== Some initial exploration ===")
    cur.execute("SELECT year, COUNT(*) FROM rankings GROUP BY year;")
    print("Counts by year:", cur.fetchall())

    # --- (C) Insert Duke Tech in 2014 ---
    print("\nInserting Duke Tech (USA, 350, 60.5, 2014)...")
    cur.execute("""
        INSERT INTO rankings (institution, country, world_rank, score, year)
        VALUES (?, ?, ?, ?, ?);
    """, ("Duke Tech", "USA", 350, 60.5, 2014))
    conn.commit()

    # Verify insertion
    cur.execute("SELECT * FROM rankings WHERE institution = 'Duke Tech' AND year = 2014;")
    print("Inserted row:", cur.fetchall())

    # --- (R) Query: how many from Japan in top 200 in 2013 ---
    cur.execute("""
        SELECT COUNT(*) FROM rankings
        WHERE country = 'Japan' AND year = 2013 AND world_rank <= 200;
    """)
    cnt = cur.fetchone()[0]
    print("Japan universities in top 200 in 2013:", cnt)

    # --- (U) Update Oxford 2014 score +1.2 ---
    print("\nUpdating University of Oxford 2014 score +1.2...")
    cur.execute("""
        UPDATE rankings
        SET score = score + 1.2
        WHERE institution = 'University of Oxford' AND year = 2014;
    """)
    conn.commit()
    # Verify update
    cur.execute("""
        SELECT institution, year, score FROM rankings
        WHERE institution = 'University of Oxford' AND year = 2014;
    """)
    print("After update:", cur.fetchall())

    # --- (D) Delete 2015 universities with score < 45 ---
    print("\nDeleting 2015 universities with score < 45...")
    cur.execute("""
        DELETE FROM rankings
        WHERE year = 2015 AND score < 45;
    """)
    # It’s good to know how many rows are deleted:
    deleted = conn.total_changes  # or track change differences
    conn.commit()
    print("Deleted rows count (cumulative):", deleted)

    # Optionally, show remaining rows for 2015
    cur.execute("SELECT COUNT(*) FROM rankings WHERE year = 2015;")
    print("Remaining 2015 rows:", cur.fetchone()[0])

    cur.close()
    conn.close()
    print("\nDone.")

if __name__ == "__main__":
    main()
