import duckdb

# Database path
db_path = "/home/siva/Desktop/work/claude/first_project/file_insect.duckdb"

def read_all_logs():
    con = duckdb.connect(db_path)
    try:
        data = con.execute("SELECT * FROM file_logs").fetchall()
        columns = [desc[0] for desc in con.description]
        print(f"Columns: {columns}")
        for row in data:
            print(row)
    except Exception as e:
        print(f"Error reading database: {e}")
    finally:
        con.close()

if __name__ == "__main__":
    print("Reading data from file_logs table:")
    read_all_logs()
