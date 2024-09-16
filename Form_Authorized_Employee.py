import mysql.connector
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit
from PyQt5 import uic
from Form_Main_Employee import Form_Main_Employee
from Form_Authorized_Users import Form_Authorized_Users
import MessageBox


class Form_Authorized_Employee(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('Form_Authorized_Employee.ui', self)  # Загружаем форму Form_Authorized_Employee
        self.Design_Form_Authorized()  # Функция дизайна

        # Работа с формой Form_Authorized
        self.btnconnect.clicked.connect(self.Connection_to_Database)
        self.btnUser.clicked.connect(self.User_to_Database)

    def Design_Form_Authorized(self):
        # Установка свойства EchoMode для скрытия введенного текста
        self.lineE_password.setEchoMode(QLineEdit.Password)

        # Заполняем сразу данные в ячейки Form_Authorized
        self.lineE_user.setText('major_accounter')
        self.lineE_password.setText('yulia1990')

        # Установка цвета фона для формы
        self.setStyleSheet("background-color: BurlyWood;")

        # Работа с дизайном формы
        border = "2px"
        border_radius = "10px"
        border_color = "Wheat"

        # Работа с lineEdit
        self.lineE_user.setStyleSheet(f"border: {border} solid {border_color}; border-radius: {border_radius};")
        self.lineE_password.setStyleSheet(f"border: {border} solid {border_color}; border-radius: {border_radius};")

        # Работа с кнопками
        self.btnconnect.setStyleSheet(f"border: {border} solid {border_color}; border-radius: {border_radius};")
        self.btnUser.setStyleSheet(f"border: {border} solid {border_color}; border-radius: {border_radius};")

    def Connection_to_Database(self):
        login = self.lineE_user.text()
        password = self.lineE_password.text()

        try:
            connection = mysql.connector.connect(
                host='localhost',
                port=3306,
                user='root',
                password='25072004',
                database='data_control',
                charset='utf8mb4',
                collation='utf8mb4_unicode_ci'
            )

            cursor = connection.cursor()
            cursor.execute("SELECT * FROM Privileged_Users WHERE Логин = %s AND Пароль = %s", (login, password))
            result = cursor.fetchone()

            if result:
                self.close()  # Закрываем текущую форму
                self.Form_Main_Employee = Form_Main_Employee(connection)
                self.Form_Main_Employee.show()
            else:
                MessageBox.Message_Warning("Неверный логин или пароль!")

        except Exception as e:
            MessageBox.Message_Warning(f"Ошибка: {e}")

    def User_to_Database(self):
        try:
            connection = mysql.connector.connect(
                host='localhost',
                port=3306,
                user='root',
                password='25072004',
                database='data_control',
                charset = 'utf8mb4',
                collation = 'utf8mb4_unicode_ci'
            )
            # Закрываем форму после подключения
            self.close()
            # Открываем форму MainUser после успешного подключения
            self.form_user = Form_Authorized_Users(connection)
            self.form_user.show()
        except Exception as Error:
            MessageBox.Message_Warning(f"Ошибка: {Error}")


if __name__ == "__main__":
    try:
        app = QApplication([])
        ConnectionWindow = Form_Authorized_Employee()
        ConnectionWindow.show()
        app.exec_()
    except Exception as Error:
        MessageBox.Message_Info(Error)
