import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import psycopg2
from config import host, user, password, db_name


# Сохранение кейса в бд
def save_testcase(name, description, steps):
    try:
        # Подключение к базе данных
        con = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        with con.cursor() as cursor:
            # Вставка тесткейса и получение его id
            cursor.execute(
                "INSERT INTO testcases (name, description, created_at, uploadet_at) VALUES (%s, %s, %s, %s) RETURNING "
                "id_case",
                (name, description, datetime.now(), datetime.now())
            )
            testcase_id = cursor.fetchone()[0]

            # Вставка шагов тесткейса
            for step_number, (action_description, expected_result) in enumerate(steps, start=1):
                cursor.execute(
                    "INSERT INTO testcase_steps (stepnumber, actiondescription, expectedresult, testcaseid) VALUES ("
                    "%s, %s, %s, %s)",
                    (step_number, action_description, expected_result, testcase_id)
                )

            con.commit()
        print("[INFO] Testcase and steps saved successfully")
    except Exception as _ex:
        print("[INFO] Error while working with PostgreSQL", _ex)
    finally:
        if con:
            con.close()
            print("[INFO] PostgreSQL connection closed")


# Функция для обработки данных формы создания кейсов

def create_error_message():
    new_widow = tk.Toplevel()
    new_widow.title("Ошибка")
    new_widow.geometry("300x100")
    new_widow.resizable(False, False)

    label = tk.Label(new_widow,
                     text="База данных отсутствует! Нажмите на кнопку"
                          " ещё раз и перечитайте сообщение!", wraplength=250)
    label.pack(pady=10, padx=10)


def create_testcase_window(width=600, height=400):
    def add_step(step_num):
        # Создаем текстовое поле для ввода шага и ожидаемого результата
        step_label = tk.Label(steps_frame, text=f"Шаг {step_num}:")
        step_label.grid(row=step_num, column=0, sticky="w")
        step_entry = tk.Entry(steps_frame, width=50)
        step_entry.grid(row=step_num, column=1, padx=5, pady=5, sticky="we")
        result_label = tk.Label(steps_frame, text="Ожидаемый результат:")
        result_label.grid(row=step_num, column=2, sticky="w")
        result_entry = tk.Entry(steps_frame, width=50)
        result_entry.grid(row=step_num, column=3, padx=5, pady=5, sticky="we")

        # Добавляем созданные виджеты в список для дальнейшего управления
        steps_widgets.append((step_label, step_entry, result_label, result_entry))

        # Увеличиваем счетчик шагов
        num_steps[0] += 1

    # Создаем диалоговое окно для ввода тесткейса
    testcase_window = tk.Toplevel(root)
    testcase_window.title("Создание тесткейса")

    # Установка начального размера окна
    testcase_window.geometry(f"{width}x{height}")

    # Создаем поля для ввода названия, предусловия и описания

    tk.Label(testcase_window, text="Название:").grid(row=0, column=0, sticky="w")
    name_entry = tk.Entry(testcase_window)
    name_entry.grid(row=0, column=1, padx=10, pady=5, sticky="we")

    tk.Label(testcase_window, text="Предусловия:").grid(row=1, column=0, sticky="w")
    precondition_entry = tk.Entry(testcase_window)
    precondition_entry.grid(row=1, column=1, padx=10, pady=5, sticky="we")

    tk.Label(testcase_window, text="Описание:").grid(row=2, column=0, sticky="w")
    description_entry = tk.Entry(testcase_window)
    description_entry.grid(row=2, column=1, padx=10, pady=5, sticky="we")

    # Фрейм для шагов прохождения и ожидаемых результатов
    steps_frame = tk.Frame(testcase_window)
    steps_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")

    # Кнопка для добавления шагов
    add_step_button = tk.Button(testcase_window, text="Добавить шаг", command=lambda: add_step(num_steps[0] + 1))
    add_step_button.grid(row=4, column=0, columnspan=2, pady=10)

    # Список для хранения виджетов шагов
    steps_widgets = []

    # Счетчик шагов
    num_steps = [0]

    def save_testcase():
        # Собираем информацию о тесткейсе
        testcase = {
            "Название": name_entry.get(),
            "Предусловия": precondition_entry.get(),
            "Описание": description_entry.get(),
            "Шаги прохождения и ожидаемые результаты": []
        }
        for step_label, step_entry, result_label, result_entry in steps_widgets:
            step = step_entry.get()
            result = result_entry.get()
            if step and result:  # Убедимся, что оба поля заполнены
                testcase["Шаги прохождения и ожидаемые результаты"].append((step, result))

        print("Введенный тесткейс:")
        for key, value in testcase.items():
            print(f"{key}: {value}")

    # Кнопка для сохранения тесткейса
    save_button = tk.Button(testcase_window, text="Сохранить", command=save_testcase)
    save_button.grid(row=5, column=0, columnspan=2, pady=10)

    # Настройка растягивания виджетов при изменении размеров окна
    testcase_window.columnconfigure(1, weight=1)
    steps_frame.columnconfigure(1, weight=1)
    steps_frame.columnconfigure(3, weight=1)
    steps_frame.rowconfigure(num_steps[0] + 1, weight=1)

    # Минимальные размеры для текстовых полей описания
    description_entry.config(width=50)


def main():
    global root
    root = tk.Tk()

    # Размерность окна
    root.geometry("800x700")

    root.title("RED DWARF")

    tab_control = ttk.Notebook(root)

    # Вкладка 1
    tab1 = ttk.Frame(tab_control)
    tab_control.add(tab1, text="Главная")

    # Загрузка изображения на вкладку 1
    image = Image.open("dwarf.jpeg")
    photo = ImageTk.PhotoImage(image)

    # Отображение изображения на вкладке 1
    label1 = tk.Label(tab1, image=photo)
    label1.image = photo  # Сохраните ссылку на изображение
    label1.pack(pady=10, padx=10)

    # Вкладка 2
    tab2 = ttk.Frame(tab_control)
    tab_control.add(tab2, text="База")

    # Размещение копок
    frame_btn = tk.Frame(tab2
                         )
    frame_btn.pack(side=tk.LEFT, anchor=tk.NW, padx=10, pady=10)

    button_create = tk.Button(frame_btn, text="Создать тест-кейс",
                              command=create_testcase_window)
    button_create.pack(pady=5, padx=5)

    button = tk.Button(tab2, text="Подключение к БД",
                       command=create_error_message)
    button.pack(pady=10, padx=10)

    tab_control.pack(expand=1, fill="both")

    root.mainloop()


if __name__ == "__main__":
    main()
