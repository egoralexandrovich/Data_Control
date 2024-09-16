from PyQt5.QtWidgets import QMainWindow, QLineEdit, QTableWidgetItem
from PyQt5 import uic
from Form_Main_User import Form_Main_User
import MessageBox

class Form_Authorized_Users(QMainWindow):
    def __init__(self, connection):
        super().__init__()
        uic.loadUi('Form_Authorized_Users.ui', self)  # Загружаем форму Form_Authorized
        self.connection = connection  # Принятие объекта соединения в конструкторе
        self.login = None
        self.password = None
        self.Design_Form_Authorized() # Функция дизайна

        # Работа с кнопкой подключение
        self.btnconnect.clicked.connect(self.Connection_to_DataBase)
        self.btnEmployee.clicked.connect(self.Employee_to_DataBase)

    def Design_Form_Authorized(self):
        # Установка свойства EchoMode для скрытия введенного текста
        self.lineE_password.setEchoMode(QLineEdit.Password)

        # Установим значения для login и password
        self.lineE_login.setText("yulia")
        self.lineE_password.setText("yulechka1998")

        # Установка цвета фона для формы
        self.setStyleSheet("background-color: BurlyWood;")

        # Работа с дизайном формы
        border = "2px"
        border_radius = "10px"
        border_color = "Wheat"

        # Работа с lineEdit
        self.lineE_login.setStyleSheet(f"border: {border} solid {border_color}; border-radius: {border_radius};")
        self.lineE_password.setStyleSheet(f"border: {border} solid {border_color}; border-radius: {border_radius};")

        # Работа с кнопками
        self.btnconnect.setStyleSheet(f"border: {border} solid {border_color}; border-radius: {border_radius};")
        self.btnEmployee.setStyleSheet(f"border: {border} solid {border_color}; border-radius: {border_radius};")

    def Connection_to_DataBase(self):
        try:
            # Создаем подключение
            connection = self.connection
            cursor = connection.cursor()

            # SQL-запрос для выбора всех строк из таблицы Customers
            cursor.execute("SELECT Логин, Пароль FROM Customers")

            # Получаем все строки результата
            rows = cursor.fetchall()

            is_authorized = False  # Флаг авторизации

            for row in rows:
                login = row[0].strip()  # Значение столбца "Логин" с удалением пробелов
                password = row[1].strip()  # Значение столбца "Пароль" с удалением пробелов

                # Получаем текст из QLineEdit
                entered_login = self.lineE_login.text().strip()
                entered_password = self.lineE_password.text().strip()

                # Сравниваем значения с введенными данными
                if login == entered_login and password == entered_password:
                    is_authorized = True  # Пользователь авторизован
                    # Закрываем форму
                    self.close()

                    # Действия при совпадении
                    self.form_users = Form_Main_User(connection, entered_login, entered_password)
                    self.form_users.show()
                    break  # Выходим из цикла, так как пользователь найден

            if is_authorized == False:
                MessageBox.Message_Warning("Пользователя с такими данными не существует!")

        except Exception as Error:
            MessageBox.Message_Warning(f"Ошибка: {Error}")

    def Employee_to_DataBase(self):
        try:
            # Закрываем форму
            self.close()

            # Возвращаемся на форму Form_Authorized
            from Form_Authorized_Employee import Form_Authorized_Employee
            self.form_authorized_employee = Form_Authorized_Employee()
            self.form_authorized_employee.show()
        except Exception as Error:
            MessageBox.Message_Warning(f"Ошибка: {Error}")
