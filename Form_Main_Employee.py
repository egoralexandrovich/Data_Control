from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QTableWidget
from PyQt5 import uic
from Form_Customers import Form_Customers
import MessageBox


class Form_Main_Employee(QMainWindow):
    def __init__(self, connection):
        super().__init__()
        uic.loadUi('Form_Main_Employee.ui', self)  # Загружаем форму
        self.connection = connection  # Принятие объекта соединения в конструкторе

        # Работа с функциями
        self.Design_Form_Main()  # Функция дизайна формы
        self.TestData()  # Тестовые данные

        # Работа с таблицей
        self.tableWidget = self.findChild(QTableWidget, "table_Info")  # Находим виджет table_Info из .ui файла

        # Работа с кнопками
        self.btnLoadData.clicked.connect(self.LoadData_in_Table)
        self.btnPerformQuery.clicked.connect(self.PerformQuery)
        self.btnFormCustomers.clicked.connect(self.Form_Customers)

        # Работа с формами
        self.btnExit.clicked.connect(self.Exit)

    def Design_Form_Main(self):
        # Установка цвета фона для формы
        self.setStyleSheet("background-color: BurlyWood;")

        # Работа с дизайном формы
        border = "2px"
        border_radius = "10px"
        border_color = "Wheat"

        # Работа с lineEdit
        self.lineE_NameTable.setStyleSheet(f"border: {border} solid {border_color}; border-radius: {border_radius};")

        # Работа с textEdit
        self.textE_Query.setStyleSheet(f"border: {border} solid {border_color}; border-radius: {border_radius};")

        # Работа с кнопками
        self.btnLoadData.setStyleSheet(f"border: {border} solid {border_color}; border-radius: {border_radius};")
        self.btnPerformQuery.setStyleSheet(f"border: {border} solid {border_color}; border-radius: {border_radius};")

        self.btnFormCustomers.setStyleSheet(f"border: {border} solid {border_color}; border-radius: {border_radius};")
        self.btnFormEmployees.setStyleSheet(f"border: {border} solid {border_color}; border-radius: {border_radius};")
        self.btnFormContracts.setStyleSheet(f"border: {border} solid {border_color}; border-radius: {border_radius};")
        self.btnFormInventory.setStyleSheet(f"border: {border} solid {border_color}; border-radius: {border_radius};")
        self.btnFormDecommissionedInventory.setStyleSheet(f"border: {border} solid {border_color}; border-radius: {border_radius};")
        self.btnFormHistory.setStyleSheet(f"border: {border} solid {border_color}; border-radius: {border_radius};")
        self.btnFormActs.setStyleSheet(f"border: {border} solid {border_color}; border-radius: {border_radius};")
        self.btnFormPayments.setStyleSheet(f"border: {border} solid {border_color}; border-radius: {border_radius};")
        self.btnFormAccounts.setStyleSheet(f"border: {border} solid {border_color}; border-radius: {border_radius};")
        self.btnFormPrivilegedUsers.setStyleSheet(f"border: {border} solid {border_color}; border-radius: {border_radius};")
        self.btnExit.setStyleSheet(f"border: {border} solid {border_color}; border-radius: {border_radius};")

    def TestData(self):
        # Подключение к базе данных
        connection = self.connection
        cursor = connection.cursor()

        # Получение данных из таблицы Customers
        cursor.execute("SELECT Наименование_ОС, Место_хранения, Количество_ОС, Стоимость_аренды_за_единицу FROM Inventory")
        data = cursor.fetchall()

        # Получение названий столбцов
        column_names = [description[0] for description in cursor.description]

        # Установка количества строк и столбцов в QTableWidget
        self.table_Info.setRowCount(len(data))
        self.table_Info.setColumnCount(len(column_names))

        # Установка названий столбцов в QTableWidget
        self.table_Info.setHorizontalHeaderLabels(column_names)

        # Добавление данных в QTableWidget
        for row_num, row_data in enumerate(data):
            for col_num, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                self.table_Info.setItem(row_num, col_num, item)

        # Изменим размер столбцов и строк, чтобы они соответствовали содержимому
        self.table_Info.resizeColumnsToContents()
        self.table_Info.resizeRowsToContents()

        # Устанавливаем цвет фона для таблицы
        self.table_Info.setStyleSheet("background-color: BurlyWood")

    def LoadData_in_Table(self):
        try:
            # Подключаемся к базе данных
            connection = self.connection
            cursor = connection.cursor()

            # Считываем имя таблицы
            data_base = self.lineE_NameTable.text()

            # Выполняем запрос к таблице для получения строк и столбцов
            query = f"SELECT * FROM {data_base}"
            cursor.execute(query)

            rows = cursor.fetchall()

            # Получаем имена столбцов из описания курсурсурсора
            column_names = [desc[0] for desc in cursor.description]

            # Очищаем таблицу перед загрузкой данных
            self.tableWidget.setRowCount(0)
            self.tableWidget.setColumnCount(len(column_names))

            # Устанавливаем имена столбцов в качестве заголовков
            self.tableWidget.setHorizontalHeaderLabels(column_names)

            # Загружаем данные в таблицу
            for row_index, row_data in enumerate(rows):
                self.tableWidget.insertRow(row_index)
                for column_index, column_data in enumerate(row_data):
                    self.tableWidget.setItem(row_index, column_index, QTableWidgetItem(str(column_data)))

            # Изменим размер столбцов и строк, чтобы они соответствовали содержимому
            self.tableWidget.resizeColumnsToContents()
            self.tableWidget.resizeRowsToContents()

            # Очищаем строку после загрузки данных
            self.lineE_NameTable.setText("")

        except Exception as Error:
            MessageBox.Message_Warning(f"Ошибка: {Error}")

    def PerformQuery(self):
        try:
            # Импортируем соединение
            connection = self.connection
            cursor = connection.cursor()

            query = self.textE_Query.toPlainText()  # Считываем текст из строки

            # Очищаем таблицу перед выводом результатов
            self.tableWidget.setRowCount(0)
            self.tableWidget.setColumnCount(0)

            # Проверяем, содержит ли запрос слово "call"
            if "call" in query.lower():
                # Вызываем процедуру
                cursor.callproc(query.split()[1])
                connection.commit()

                # Получаем данные из результата процедуры
                result = cursor.stored_results()
                for res in result:
                    # Получаем названия столбцов
                    column_names = [col[0] for col in res.description]
                    self.tableWidget.setColumnCount(len(column_names))
                    self.tableWidget.setHorizontalHeaderLabels(column_names)

                    # Получаем данные из результата процедуры
                    rows = res.fetchall()
                    self.tableWidget.setRowCount(len(rows))
                    for i, row in enumerate(rows):
                        for j, value in enumerate(row):
                            item = QTableWidgetItem(str(value))
                            self.tableWidget.setItem(i, j, item)
            else:
                # Выполняем обычный запрос
                cursor.execute(query)  # Выполняем запрос

                # Получаем заголовки столбцов
                column_names = [col[0] for col in cursor.description]
                self.tableWidget.setColumnCount(len(column_names))
                self.tableWidget.setHorizontalHeaderLabels(column_names)

                # Получаем данные из результата запроса
                rows = cursor.fetchall()
                self.tableWidget.setRowCount(len(rows))
                for i, row in enumerate(rows):
                    for j, value in enumerate(row):
                        item = QTableWidgetItem(str(value))
                        self.tableWidget.setItem(i, j, item)

            # Изменим размер столбцов и строк, чтобы они соответствовали содержимому
            self.tableWidget.resizeColumnsToContents()
            self.tableWidget.resizeRowsToContents()

        except Exception as Error:
            MessageBox.Message_Warning(f"Ошибка при выполнении запроса: {Error}")

    def Form_Customers(self):
        # Закрываем форму Main
        self.close()

        # Сохраняем экземпляр класса Form_Customers
        self.customers = Form_Customers(self.connection)
        self.customers.show()

    def Exit(self):
        try:
            # Закрытие соединения с курсором и базой данных
            self.connection.close()

            # Закрываем форму Main
            self.close()

            from Form_Authorized_Employee import Form_Authorized_Employee

            MessageBox.Message_Info("Вы были отключены от базы данных!")

            # Сохраняем экземпляр класса Form_Customers
            self.form_authorized_employee = Form_Authorized_Employee()
            self.form_authorized_employee.show()
        except Exception as Error:
            MessageBox.Message_Warning(f"Ошибка: {Error}")

