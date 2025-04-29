def create_html_table(table, row_markers, col_markers, original_message=None):
    """
    Створює HTML-таблицю з підсвічуванням літер з оригінального повідомлення.

    Args:
        table: Таблиця шифрозамін
        row_markers: Маркери рядків
        col_markers: Маркери стовпців
        original_message: Оригінальне повідомлення для підсвічування літер
    """
    # Перетворюємо оригінальне повідомлення у верхній регістр і створюємо множину унікальних літер
    if original_message:
        # Створюємо словник для підрахунку кількості кожної літери
        char_counts = {}
        for char in original_message.upper():
            if not char.isspace():  # Ігноруємо пробіли
                char_counts[char] = char_counts.get(char, 0) + 1
    else:
        char_counts = {}

    html = """
    <style>
        .cipher-table {
            border-collapse: collapse;
            width: 100%;
            margin-top: 20px;
        }
        .cipher-table th, .cipher-table td {
            border: 1px solid #dee2e6;
            padding: 8px;
            text-align: center;
            vertical-align: middle;
            position: relative;
        }
        .cipher-table th {
            background-color: #f8f9fa;
            font-weight: bold;
        }
        .highlight-char {
            background-color: #ffc107;  /* Жовтий колір підсвічування */
            color: #000;
            font-weight: bold;
        }
        .char-count {
            position: absolute;
            top: 0;
            right: 0;
            font-size: 0.7em;
            background-color: #dc3545;  /* Червоний колір для лічильника */
            color: white;
            border-radius: 50%;
            width: 16px;
            height: 16px;
            display: flex;
            align-items: center;
            justify-content: center;
            line-height: 1;
        }
    </style>
    <table class="cipher-table">
        <thead>
            <tr>
                <th></th>
    """

    # Додаємо заголовки колонок
    for col in col_markers:
        html += f"<th>{col}</th>"

    html += """
            </tr>
        </thead>
        <tbody>
    """

    # Додаємо рядки з даними
    for i, row_marker in enumerate(row_markers):
        html += f"<tr><th>{row_marker}</th>"
        for j in range(len(col_markers)):
            char = table[i][j]
            char_count = char_counts.get(char, 0)

            if char_count > 0:
                html += f'<td class="highlight-char">{char}'
                html += f'<span class="char-count">{char_count}</span>'
                html += '</td>'
            else:
                html += f"<td>{char}</td>"
        html += "</tr>"

    html += """
        </tbody>
    </table>

    <div class="legend mt-3">
        <p><i>Примітка: жовтим кольором позначено літери з оригінального повідомлення.
        Число в правому верхньому куті показує кількість входжень літери в повідомлення.</i></p>
    </div>
    """

    return html
