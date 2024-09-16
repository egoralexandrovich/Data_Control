from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import QMessageBox


def setupMessageBox(messageBox, user_data, icon_path):
    # Установка пользовательской иконки
    icon = QIcon(icon_path)
    messageBox.setIconPixmap(icon.pixmap(32, 32))  # Устанавливаем иконку размером 32x32
    messageBox.setWindowIcon(icon)

    # Установка шрифта
    font = QFont("SemiLight", 14)  # Установка шрифта SemiLight размером 14
    messageBox.setFont(font)

    # Установка текста и заголовка
    messageBox.setText(f"{user_data}")
    messageBox.setWindowTitle("Сообщение")


def Message_Info(user_data):
    messageBox = QMessageBox()
    setupMessageBox(messageBox, user_data,
                    "C:\\Users\\Егор\\PycharmProjects\\Data_Control\\Изображения\\Информация.png")

    # Отображение диалогового окна
    messageBox.exec_()


def Message_Warning(user_data):
    messageBox = QMessageBox()
    setupMessageBox(messageBox, user_data,
                    "C:\\Users\\Егор\\PycharmProjects\\Data_Control\\Изображения\\Внимание.png")

    # Отображение диалогового окна
    messageBox.exec_()


def Message_Question(user_data):
    messageBox = QMessageBox(QMessageBox.Question, "Вопрос", f"{user_data}", QMessageBox.Yes | QMessageBox.No)
    setupMessageBox(messageBox, user_data, "C:\\Users\\Егор\\PycharmProjects\\Data_Control\\Изображения\\Вопрос.png")

    # Отображение диалогового окна
    result = messageBox.exec_()
    return result
