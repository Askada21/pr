from database.connection import get_connection

def check_data_quality() -> dict:
    query = """
        select
            count(*) as total_records,

            count(*) filter (
                where inventory_level is null
                   or units_sold is null
                   or price is null
            ) as missing_critical_values,

            count(*) filter (
                where inventory_level < 0
            ) as negative_inventory,

            count(*) filter (
                where units_sold < 0
            ) as negative_sales,

            count(*) filter (
                where price <= 0
            ) as invalid_prices

        from daily_inventory
    """

    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            row = cursor.fetchone()

        return {
            "total_records": row[0],
            "missing_critical_values": row[1],
            "negative_inventory": row[2],
            "negative_sales": row[3],
            "invalid_prices": row[4],
        }

    finally:
        connection.close()

if __name__ == "__main__":
    results = check_data_quality()

    print("\nDATA QUALITY REPORT")
    print("-" * 35)

    for metric, value in results.items():
        print(f"{metric}: {value}")

    issues = sum(
        value
        for key, value in results.items()
        if key != "total_records"
    )

    if issues == 0:
        print("\nPASS: No checked data quality issues found.")
    else:
        print(f"\nWARNING: {issues} quality issues detected.")
