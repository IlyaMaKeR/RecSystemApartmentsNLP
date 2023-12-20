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
        # Формирование динамического SQL-запроса
        sql_query = "SELECT * FROM apartments WHERE "

        # Преобразование человеческих фраз в соответствующие значения
        for i, tag in enumerate(tags):
            if tag.isdigit():  # Если это число, ищем только по цене
                sql_query += f"Цена = {tag} AND "
            elif "комнат" in tag.lower():  # Если в фразе упоминаются "комнаты", добавляем в условие для количества комнат
                num_rooms = tag.split()[0]  # Получаем количество комнат
                sql_query += f"Комнат LIKE '%{num_rooms}%' AND "
            elif "площадь" in tag.lower():  # Если в фразе упоминается "площадь", ищем соответствующее значение
                area_value = float(tag.split()[0])  # Получаем значение площади
                # Используем операторы больше или равно и меньше или равно для приближенного поиска
                sql_query += f"Площадь >= {area_value - 5} AND Площадь <= {area_value + 5} AND "
            elif "цена" in tag.lower():  # Если в фразе упоминается "цена", ищем соответствующее значение
                price_value = float(tag.split()[0])  # Получаем значение цены
                # Используем операторы больше или равно и меньше или равно для приближенного поиска
                sql_query += f"Цена >= {price_value - 50000} AND Цена <= {price_value + 50000} AND "
            else:
                # Добавляем условие для каждой из ваших колонок в определенном порядке
                sql_query += f"(Площадь LIKE '%{tag}%' OR Комнат LIKE '%{tag}%' OR Цена LIKE '%{tag}%' OR Местоположение LIKE '%{tag}%' OR Комфорт LIKE '%{tag}%') AND "

        # Удаление последнего 'AND' из запроса
        sql_query = sql_query.rstrip('AND ')

        # Добавление сортировки и ограничение на 5 результатов
        sql_query += " ORDER BY ID DESC LIMIT 4"

        # Выполнение запроса
        cursor.execute(sql_query)

        # Получение результатов
        results = cursor.fetchall()

        # Преобразование результатов в список словарей
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
        # Закрытие соединения
        connector.close()
