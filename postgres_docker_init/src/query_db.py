import psycopg2

def main():
    try:
        connection = psycopg2.connect(
            dbname="customers_db",
            user="damilola_o",
            password="damidami",
            host="localhost",
            port="5434"
        )
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM customers.customer_data;")
        record_count = cursor.fetchone()[0]
        print(f"Number of records in the table: {record_count}")
    except Exception as error:
        print(f"Error connecting to the database: {error}")
    finally:
        if connection:
            cursor.close()
            connection.close()

if __name__ == "__main__":
    main()
