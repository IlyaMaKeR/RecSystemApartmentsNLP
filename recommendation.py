import pymysql


def search_apartments_by_tags(tags):
    connector = pymysql.connect(
        host="",
        user="Admin",
        password="",
        database="apartments",
        port=
    )

    cursor = connector.cursor()

    try:
        sql_query = "SELECT * FROM apartments WHERE "

        for i, tag in enumerate(tags):
            if tag.isdigit():
                sql_query += f"Цена = {tag} AND "
            elif "комнат" in tag.lower():
                num_rooms = tag.split()[0]
                sql_query += f"Комнат LIKE '%{num_rooms}%' AND "
            elif "площадь" in tag.lower():
                area_value = float(tag.split()[0])
                sql_query += f"Площадь >= {area_value - 5} AND Площадь <= {area_value + 5} AND "
            elif "цена" in tag.lower():
                price_value = float(tag.split()[0])
                sql_query += f"Цена >= {price_value - 50000} AND Цена <= {price_value + 50000} AND "
            else:
                sql_query += f"(Площадь LIKE '%{tag}%' OR Комнат LIKE '%{tag}%' OR Цена LIKE '%{tag}%' OR Местоположение LIKE '%{tag}%' OR Комфорт LIKE '%{tag}%') AND "
                
        sql_query = sql_query.rstrip('AND ')

        sql_query += " ORDER BY ID DESC LIMIT 4"

        cursor.execute(sql_query)

        results = cursor.fetchall()

        apartments = []
        for row in results:
            apartment_info = {
                'ID': row[0],
                'Площадь': row[1],
                'Комнат': row[2],
                'Цена': row[3],
                'Местоположение': row[4],
                'Комфорт': row[5],
            }
            apartments.append(apartment_info)
        return apartments



    finally:
        connector.close()
