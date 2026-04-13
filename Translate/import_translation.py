import json
import csv
import os
from tqdm import tqdm

input_book = "hoshishiro_03.book"
input_csv = "dialogues.csv"
output_book = "hoshishiro_03_ru.book"

# Проверка существования файлов
if not os.path.exists(input_book):
    print(f"Ошибка: файл {input_book} не найден!")
    exit()
if not os.path.exists(input_csv):
    print(f"Ошибка: файл {input_csv} не найден!")
    exit()

print("Загрузка JSON...")
with open(input_book, "r", encoding="utf-8") as f:
    data = json.load(f)

import_grid_list = data.get("importGridList", {})
if not import_grid_list:
    print("Ошибка: нет importGridList")
    exit()

grid_array = import_grid_list.get("Array", [])
print(f"Найдено grid-секций: {len(grid_array)}")

# Чтение CSV с отладкой
translations = {}
print("Чтение CSV с переводами...")
with open(input_csv, "r", encoding="utf-8-sig") as csvfile:
    # Сначала прочитаем первую строку, чтобы определить разделитель
    first_line = csvfile.readline()
    csvfile.seek(0)
    # Пробуем угадать разделитель (табуляция или запятая)
    if '\t' in first_line:
        delimiter = '\t'
    else:
        delimiter = ','
    print(f"Используемый разделитель: '{delimiter}'")
    
    reader = csv.DictReader(csvfile, delimiter=delimiter)
    print("Колонки в CSV:", reader.fieldnames)
    
    for i, row in enumerate(reader):
        if i < 5:  # выводим первые 5 строк для проверки
            print(f"Строка {i}: {row}")
        row_idx = row.get("rowIndex", "")
        russian = row.get("russian", "").strip()
        if row_idx.isdigit() and russian:
            row_idx = int(row_idx)
            translations[row_idx] = russian

print(f"Загружено переводов: {len(translations)}")

# Обновление строк в JSON
total_updated = 0
for grid_idx, grid in enumerate(tqdm(grid_array, desc="Обработка grid-секций")):
    rows_obj = grid.get("rows", {})
    rows_array = rows_obj.get("Array", [])
    if not rows_array:
        continue

    for row in rows_array:
        row_idx = row.get("rowIndex")
        if row_idx is not None and row_idx in translations:
            strings_obj = row.get("strings", {})
            strings = strings_obj.get("Array", [])
            while len(strings) < 13:
                strings.append("")
            strings[12] = translations[row_idx]
            row["strings"]["Array"] = strings
            total_updated += 1

print(f"Обновлено строк: {total_updated}")

# Сохранение нового файла
print("Сохранение нового файла...")
# Сохраняем на рабочий стол, чтобы избежать проблем с правами
output_path = os.path.join(os.path.expanduser("~"), "Desktop", "hoshishiro_03_ru.book")
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Готово! Новый файл: {output_path}")