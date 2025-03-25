import subprocess


def run_student_code(code_file, input_data, timeout=5):
    """
    Запускает код ученика и возвращает stdout.
    :param code_file: Путь к файлу с кодом ученика.
    :param input_data: Входные данные для программы (опционально).
    :param timeout: Время ожидания выполнения программы (в секундах).
    :return: Вывод программы (stdout).
    """
    with open(code_file, "r", encoding='UTF-8') as f:
        code_src = f.read()
        if "exec" in code_src or "import" in code_src:
            return f"Запрещенные конструкции в коде."
            
    try:
        result = subprocess.run(
            ["python", code_file],
            input=input_data,
            text=True,
            capture_output=True,
            timeout=timeout,
        )
        if result.returncode != 0:
            return f"Ошибка выполнения: {result.stderr}"
        return result.stdout
    except subprocess.TimeoutExpired:
        return "Ошибка: время выполнения программы истекло."
    except Exception as e:
        return f"Ошибка: {str(e)}"

if __name__ == "__main__":
    code_file = 'sc.py'
    input_data = 'digits.txt'
    ret = run_student_code(code_file, input_data)
    print(ret)
