from flask import Flask, request, render_template_string
import cups
import os

app = Flask(__name__)

# Подключение к CUPS
conn = cups.Connection()

# Главная страница с формой для загрузки файла
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Получаем загруженный файл
        file = request.files['file']
        printer_name = request.form['printer']

        # Сохраняем файл во временную директорию
        file_path = f"/tmp/{file.filename}"
        file.save(file_path)

        # Печатаем файл
        conn.printFile(printer_name, file_path, file.filename, {})

        # Удаляем временный файл
        os.remove(file_path)

        return "Файл отправлен на печать!"

    # Получаем список принтеров
    printers = conn.getPrinters()
    return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Печать файлов</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background-color: #1e1e1e;
                    color: #ffffff;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    margin: 0;
                }
                .container {
                    background-color: #333;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
                }
                label {
                    display: block;
                    margin-bottom: 8px;
                }
                input[type="file"], select, input[type="submit"] {
                    width: 100%;
                    padding: 10px;
                    margin-bottom: 10px;
                    border: none;
                    border-radius: 4px;
                }
                input[type="submit"] {
                    background-color: #5cb85c;
                    color: #ffffff;
                    cursor: pointer;
                }
                input[type="submit"]:hover {
                    background-color: #4cae4c;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <form method="post" enctype="multipart/form-data">
                    <label for="file">Выберите файл для печати:</label>
                    <input type="file" name="file" required>
                    <label for="printer">Выберите принтер:</label>
                    <select name="printer">
                        {% for printer in printers %}
                            <option value="{{ printer }}">{{ printer }}</option>
                        {% endfor %}
                    </select>
                    <input type="submit" value="Печать">
                </form>
            </div>
        </body>
        </html>
    ''', printers=printers.keys())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
