import os
import stat
import shutil

# Шаг 1: Создание папки с ограниченными правами
folder_name = 'restricted_folder'
os.makedirs(folder_name, exist_ok=True)

# Установка прав на папку (только для владельца)
os.chmod(folder_name, stat.S_IRUSR | stat.S_IWUSR)

# Шаг 2: Помещение файла пользователя и файла данных в папку
user_file_path = os.path.join(folder_name, 'user_file.txt')
data_file_path = os.path.join(folder_name, 'data_file.txt')

with open(user_file_path, 'w') as user_file:
    user_file.write('Это файл пользователя.')

with open(data_file_path, 'w') as data_file:
    data_file.write('Это файл данных.')

# Шаг 3: Запуск кода в песочнице
# В этом примере мы просто читаем файлы и выводим их содержимое
try:
    with open(user_file_path, 'r') as user_file:
        user_content = user_file.read()
    
    with open(data_file_path, 'r') as data_file:
        data_content = data_file.read()
    
    print('Содержимое файла пользователя:')
    print(user_content)
    
    print('Содержимое файла данных:')
    print(data_content)

except Exception as e:
    print(f'Ошибка при доступе к файлам: {e}')

# Шаг 4: Удаление папки с файлами
shutil.rmtree(folder_name)
print(f'Папка {folder_name} была удалена.')

