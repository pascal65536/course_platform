import subprocess
import telebot
import random
import subprocess
import os
import sys
import json


# Вставьте ваш токен сюда
bot = telebot.TeleBot(TOKEN)
commands_dct = dict()


def run_student_code(code_file, input_data, timeout=5):
    """
    Запускает код ученика и возвращает stdout.
    :param code_file: Путь к файлу с кодом ученика.
    :param input_data: Входные данные для программы (опционально).
    :param timeout: Время ожидания выполнения программы (в секундах).
    :return: Вывод программы (stdout).
    """
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


def check_solution(test_cases, code_file):
    """
    Проверяет решение ученика на нескольких тестовых случаях.
    :param test_cases: Список тестовых случаев.
    :param code_file: Путь к файлу с кодом ученика.
    :return: Результаты проверки.
    """
    results = {"passed": 0, "failed": 0, "errors": 0, "details": []}

    for i, test_case in enumerate(test_cases, 1):
        input_data = test_case.get("input", "")
        expected_output = test_case.get("output", "")
        description = test_case.get("description", f"Тест {i}")

        student_output = run_student_code(code_file, input_data)

        if "Ошибка" in student_output:
            results["errors"] += 1
            results["details"].append(
                {
                    "test": description,
                    "status": "error",
                    "expected": expected_output,
                    "received": student_output,
                }
            )
        elif student_output.strip() == expected_output.strip():
            results["passed"] += 1
            results["details"].append(
                {
                    "test": description,
                    "status": "passed",
                    "expected": expected_output,
                    "received": student_output,
                }
            )
        else:
            results["failed"] += 1
            results["details"].append(
                {
                    "test": description,
                    "status": "failed",
                    "expected": expected_output,
                    "received": student_output,
                }
            )

    return results


def run_tests_(code):
    code_file = "student_code.py"
    with open(code_file, "w") as f:
        f.write(code)

    test_cases = [
        {
            "input": "5\n3",
            "output": "8\n",
            "description": "Проверка сложения двух чисел",
        },
        {
            "input": "10\n-2",
            "output": "8\n",
            "description": "Проверка сложения с отрицательным числом",
        },
    ]
    results = check_solution(test_cases, code_file)

    msg_lst = list()
    msg_lst.append(f"Пройдено тестов: {results['passed']}")
    msg_lst.append(f"Не пройдено тестов: {results['failed']}")
    msg_lst.append(f"Ошибок: {results['errors']}")
    msg_lst.append(f"\n")
    for detail in results["details"]:
        msg_lst.append(f"Тест: {detail['test']}")
        msg_lst.append(f"Статус: {detail['status']}")
        msg_lst.append(f"Ожидалось: {detail['expected']}".strip())
        msg_lst.append(f"Получено: {detail['received']}".strip())
        msg_lst.append(f"\n")
    return "\n".join(msg_lst)


def run_tests(code_file):
    try:
        # Запускаем тесты с помощью pytest
        result = subprocess.run(
            ["pytest", code_file],
            capture_output=True,
            text=True,
        )
        return result.stdout + "\n" + result.stderr

    except Exception as e:
        return f"Ошибка при выполнении кода: {str(e)}"


@bot.message_handler(commands=["start"])
def start_game(message):
    username = message.from_user.username
    msg = f"Привет, {username}. Привет! Отправь мне свой код для проверки."
    bot.send_message(message.chat.id, msg, parse_mode="html")


@bot.message_handler(func=lambda message: True)
def code_message(message):
    text = message.text
    code_file = "student_code.py"
    with open(code_file, "w") as f:
        f.write(text)
    result = run_student_code(code_file, '10\n20')
    # result = run_tests(text)

    print(result)
    # result = '<code>' + result + '</code>'
    # bot.reply_to(message, result, parse_mode="html")


if __name__ == "__main__":
    bot.polling(none_stop=True)
