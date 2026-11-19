from database.connection import get_connection


def main():
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "select current_database(), current_user;"
            )

            result = cursor.fetchone()

            print("Database connection successful!")
            print("Database:", result[0])
            print("User:", result[1])

    finally:
        connection.close()


if __name__ == "__main__":
    main()