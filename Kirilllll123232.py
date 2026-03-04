# with open("test.txt", "w") as file:
#     file.write("Привет файл!")
# with open("test.txt", "r") as file:
#     content = file.read()
#     print(content)

# with open("numbers.txt", "w") as file:
#     for number in range(1, 11):
#         file.write(f"{number}\n")
# total_sum = 0
# with open("numbers.txt", "r") as file:
#     for line in file:
#         total_sum += int(line.strip())
#     print("Сумма чисел от 1 до 10", total_sum)

# lines = ()
# for i in range(5):
#     line = input(f"Введите строку {i+1}:")
#     lines.append(line)
# with open("user_text.txt", "w", encoding="utf-8") as file:
#     for line in lines:
#         file.write(line + "\n")
# with open("user_text.txt", "r", encoding="utf-8") as file:
#     print("\nСтроки длинне 5 символов:")
#     for line in file:
#         if len(line.strip()) > 5:
#             print(line.strip())

# with open('data.txt', 'r', encoding="utf-8") as file:
#     lines = file.readlines()
#     line_count = len(lines)
#     print(f'Количество строк в файле:'{lines_count})

# with open("log.txt", "a") as file:
#     file.write("Первая строка\n")
#     file.write("Вторая строка\n")
#     file.write("Третья строка\n")
# with open("log.txt", "r", encoding="utf-8") as file:
#     content = file.read()
#     print("Содержащие файлы:")
#     print(content)

# with open("numbers.txt", "r", encoding="utf-8") as file:
#     numbers = list(map(int, file.read().split()))

# maximum = max(numbers)
# minimum = min(numbers)

# print("Максимально число:", maximum)
# print("Минимально число:", minimum)

# with open("source.txt", "r", encoding="utf-8") as src:
#     content = scr.read()
# with open("copy.txt", "w", encoding="utf-8") as dst:
#     dst.write(content)
# print("Файл успешно скопирован")

# with open("input.txt", "r", encoding="utf-8") as src:
#     text = src.read()
# upper_text = text.upper()
# with open("output.txt", "w", encoding="utf-8") as dst:
#     dst.write(upper_text)
# print("Файл создан. Текст переведен в верхний регистр.")

import json

person = {"Имя": "Иван", "Возраст": 25, "Город": "Москва"}
with open("person.json", "w", encoding="utf-8") as file:
    json.dump(person, file, ensure_ascii=False, indent=4)

print("JSON-Файл создан")
