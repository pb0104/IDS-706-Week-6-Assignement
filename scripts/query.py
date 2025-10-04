import os
import sqlite3
import pandas as pd

def main():
    # Path to the DB (adjust if needed)
    db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'university_database.db')
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    print("=== INITIAL DATA EXPLORATION ===\n")

    # Helper function to run SQL and display using pandas
    def run_query(query, description):
        print(f"\n--- {description} ---")
        df = pd.read_sql_query(query, conn)
        print(df.head(10))

    # Initial Exploration Queries

    # View first 10 records
    run_query("SELECT * FROM university_rankings LIMIT 10;", "First 10 Records")

    # How many universities appear in multiple years
    run_query("""
        SELECT institution, COUNT(DISTINCT year) AS years_present
        FROM university_rankings
        GROUP BY institution
        HAVING COUNT(DISTINCT year) > 1
        ORDER BY years_present DESC, institution
        LIMIT 10;
    """, "Universities in Multiple Years")

    # Average rank per country in 2015
    run_query("""
        SELECT country,
               ROUND(AVG(world_rank), 2) AS avg_rank_2015
        FROM university_rankings
        WHERE year = 2015
        GROUP BY country
        ORDER BY avg_rank_2015 ASC
        LIMIT 10;
    """, "Average Rank per Country in 2015")

    # Year-over-year change in average score
    run_query("""
        WITH yearly_avg AS (
            SELECT year, AVG(score) AS avg_score
            FROM university_rankings
            GROUP BY year
        )
        SELECT a.year,
               ROUND(a.avg_score, 2) AS avg_score,
               ROUND(a.avg_score - b.avg_score, 2) AS change_from_last_year
        FROM yearly_avg a
        LEFT JOIN yearly_avg b
             ON a.year = b.year + 1
        ORDER BY a.year;
    """, "Year-over-Year Change in Average Score")

    print("\n=== CRUD OPERATIONS ===")
    # --- (C) Insert Duke Tech in 2014 ---
    print("\n\n=== INSERT OPERATION ===")
    print("Inserting Duke Tech (USA, 350, 60.5, 2014)...")
    cur.execute("""
        INSERT INTO university_rankings (institution, country, world_rank, score, year)
        VALUES (?, ?, ?, ?, ?);
    """, ("Duke Tech", "USA", 350, 60.5, 2014))
    conn.commit()

    # Verify insertion
    cur.execute("SELECT * FROM university_rankings WHERE institution = 'Duke Tech' AND year = 2014;")
    print("Inserted row:", cur.fetchall())

    # --- (R) Count Japanese universities in top 200 in 2013 ---
    print("\n=== READ OPERATION ===")
    print("Counting Japan universities in top 200 in 2013...")
    cur.execute("""
        SELECT COUNT(*) FROM university_rankings
        WHERE country = 'Japan' AND year = 2013 AND world_rank <= 200;
    """)
    cnt = cur.fetchone()[0]
    print("Japan universities in top 200 in 2013:", cnt)

    # --- (U) Update Oxford 2014 score +1.2 ---
    print("\n=== UPDATE OPERATION ===")
    print("Updating University of Oxford 2014 score +1.2...")
    cur.execute("""
        SELECT institution, year, score FROM university_rankings
        WHERE institution = 'University of Oxford' AND year = 2014;
    """)
    print("Before update:", cur.fetchall())

    cur.execute("""
        UPDATE university_rankings
        SET score = score + 1.2
        WHERE institution = 'University of Oxford' AND year = 2014;
    """)
    conn.commit()

    # Verify update
    cur.execute("""
        SELECT institution, year, score FROM university_rankings
        WHERE institution = 'University of Oxford' AND year = 2014;
    """)
    print("After update:", cur.fetchall())

    # --- (D) Delete 2015 universities with score < 45 ---
    print("\n=== DELETE OPERATION ===")
    print("Deleting 2015 universities with score < 45...")
    cur.execute("""
        DELETE FROM university_rankings
        WHERE year = 2015 AND score < 45;
    """)
    deleted = conn.total_changes
    conn.commit()
    print("Deleted rows count (cumulative):", deleted)

    # Verify deletion of low-score 2015 universities
    cur.execute("SELECT COUNT(*) FROM university_rankings WHERE year = 2015 AND score < 45;")
    print("Remaining 2015 rows with score < 45:", cur.fetchone()[0])

    # Remaining 2015 rows
    cur.execute("SELECT COUNT(*) FROM university_rankings WHERE year = 2015;")
    print("Remaining 2015 rows:", cur.fetchone()[0])

    cur.close()
    conn.close()
    print("\n=== DONE ===")

if __name__ == "__main__":
    main()
