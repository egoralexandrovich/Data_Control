from PyQt5.QtWidgets import QMainWindow, QLineEdit
from PyQt5 import uic
import MessageBox


class Form_Customers(QMainWindow):
    def __init__(self, connection):
        super().__init__()
        uic.loadUi("Form_Customers.ui", self)  # Загружаем форму
        self.connection = connection  # Принятие объекта соединения в конструкторе

        # Работа с функциями
        self.LoadData()  # Функция загрузки данных
        self.Design()  # Дизайн формы

        # Подключаем кнопки к методам
        self.btnClear.clicked.connect(self.Clear)
        self.btnAddCustomer.clicked.connect(self.AddCustomer)
        self.btnNext.clicked.connect(self.Next)
        self.btnBack.clicked.connect(self.Back)
        self.btnExit.clicked.connect(self.Exit)
        self.btnDelete.clicked.connect(self.Delete)
        self.btnCorrectly.clicked.connect(self.Correctly)
        self.btnGoCustomer.clicked.connect(self.GoCustomer)

    def Design(self):
        # Установка цвета фона для формы
        self.setStyleSheet("background-color: BurlyWood;")

        # Работа с дизайном формы
        border = "2px"
        border_radius = "10px"
        border_color = "Wheat"

        # Работа с lineEdit
        self.lineE_Name.setStyleSheet(f"border: {border} solid {border_color}; border-radius: {border_radius};")
        self.lineE_ViewCustomer.setStyleSheet(f"border: {border} solid {border_color}; border-radius: {border_radius};")
        self.lineE_Document.setStyleSheet(f"border: {border} solid {border_color}; border-radius: {border_radius};")
        self.lineE_DataDocument.setStyleSheet(f"border: {border} solid {border_color}; border-radius: {border_radius};")
        self.lineE_INN.setStyleSheet(f"border: {border} solid {border_color}; border-radius: {border_radius};")
        self.lineE_KPP.setStyleSheet(f"border: {border} solid {border_color}; border-radius: {border_radius};")
        self.lineE_Requisites.setStyleSheet(f"border: {border} solid {border_color}; border-radius: {border_radius};")
        self.lineE_NumberCustomer.setStyleSheet(f"border: {border} solid {border_color}; border-radius: {border_radius};")
        self.lineE_login.setStyleSheet(f"border: {border} solid {border_color}; border-radius: {border_radius};")
        self.lineE_password.setStyleSheet(f"border: {border} solid {border_color}; border-radius: {border_radius};")

        # Работа с button
        self.btnAddCustomer.setStyleSheet(f"border: {border} solid {border_color}; border-radius: {border_radius};")
        self.btnBack.setStyleSheet(f"border: {border} solid {border_color}; border-radius: {border_radius};")
        self.btnNext.setStyleSheet(f"border: {border} solid {border_color}; border-radius: {border_radius};")
        self.btnClear.setStyleSheet(f"border: {border} solid {border_color}; border-radius: {border_radius};")
        self.btnExit.setStyleSheet(f"border: {border} solid {border_color}; border-radius: {border_radius};")
        self.btnDelete.setStyleSheet(f"border: {border} solid {border_color}; border-radius: {border_radius};")
        self.btnCorrectly.setStyleSheet(f"border: {border} solid {border_color}; border-radius: {border_radius};")
        self.btnGoCustomer.setStyleSheet(f"border: {border} solid {border_color}; border-radius: {border_radius};")

    def LoadData(self):
        connection = self.connection  # Получаем соединение
        cursor = connection.cursor()  # Создаем метод курсор для работы с БД
        try:
            # Создаем запрос к БД
            select = "SELECT * FROM Customers LIMIT 1"
            cursor.execute(select)  # Передаем запрос
            data = cursor.fetchone()  # Считываем первую строку в БД
            if data:
                # Добавляем данные в LineEdit
                self.lineE_NumberCustomer.setText(str(data[0]))
                self.lineE_Name.setText(str(data[1]))
                self.lineE_ViewCustomer.setText(str(data[2]))
                self.lineE_Document.setText(str(data[3]))
                self.lineE_DataDocument.setText(str(data[4]))
                self.lineE_INN.setText(str(data[5]))
                self.lineE_KPP.setText(str(data[6]))
                self.lineE_Requisites.setText(str(data[7]))
                self.lineE_login.setText(str(data[8]))
                self.lineE_password.setText(str(data[9]))
        except Exception as Error:
            MessageBox.Message_Warning(f"Ошибка: {Error}")

    def AddCustomer(self):
        try:
            # Получаем данные из lineEdit
            number_customer = self.lineE_NumberCustomer.text()
            name = self.lineE_Name.text()
            view_customer = self.lineE_ViewCustomer.text()
            document = self.lineE_Document.text()
            data_document = self.lineE_DataDocument.text()
            inn = self.lineE_INN.text()
            kpp = self.lineE_KPP.text()
            requisites = self.lineE_Requisites.text()
            login = self.lineE_login.text()
            password = self.lineE_password.text()

            # Создаем метод cursor
            connection = self.connection
            cursor = connection.cursor()

            try:
                # Проверяем существование записей с такими паспортными данными
                check_query = "SELECT * FROM Customers WHERE Контрагент = %s"
                cursor.execute(check_query, (number_customer,))
                existing_records = cursor.fetchall()

                if existing_records:
                    # Если записи уже существуют, выводим предупреждающее сообщение и запрашиваем подтверждение
                    confirmation = MessageBox.Message_Warning("Пользователь с такими данными уже существует!")
                else:
                    # Если записей с такими данными нет, выполняем операцию добавления без запроса подтверждения
                    insert_query = "INSERT INTO Customers (Наименование, Вид_контрагента, Идентифицирующий_документ, " \
                                   "Данные_документа, ИНН, КПП, Банковские_реквизиты, Логин, Пароль) " \
                                   "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    cursor.execute(insert_query,
                                   (name, view_customer, document, data_document, inn, kpp, requisites,
                                    login, password))
                    connection.commit()
                    MessageBox.Message_Info("Данные успешно добавлены в таблицу Customers!")
                    self.Clear()  # Очищаем данные после добавления их в таблицу

            except Exception as Error:
                MessageBox.Message_Warning(f"Ошибка при выполнении запроса к базе данных: {Error}")

        except Exception as Error:
            MessageBox.Message_Warning(f"Общая ошибка в AddCustomer: {Error}")

    def Clear(self):
        # Перебираем все QLineEdit виджеты и очищаем их текст
        for line_edit in self.findChildren(QLineEdit):
            line_edit.clear()

    def Next(self):
        connection = self.connection  # Получаем соединение
        cursor = connection.cursor()  # Создаем объект курсора для работы с БД
        try:
            number_customer = self.lineE_NumberCustomer.text()

            select = "SELECT * FROM Customers WHERE Контрагент > %s ORDER BY Контрагент LIMIT 1"
            cursor.execute(select, (number_customer,))

            row = cursor.fetchone()  # Получаем одну строку результата

            try:
                if row:  # Проверяем, что есть данные
                    self.lineE_NumberCustomer.setText(str(row[0]))
                    self.lineE_Name.setText(str(row[1]))
                    self.lineE_ViewCustomer.setText(str(row[2]))
                    self.lineE_Document.setText(str(row[3]))
                    self.lineE_DataDocument.setText(str(row[4]))
                    self.lineE_INN.setText(str(row[5]))
                    self.lineE_KPP.setText(str(row[6]))
                    self.lineE_Requisites.setText(str(row[7]))
                    self.lineE_login.setText(str(row[8]))
                    self.lineE_password.setText(str(row[9]))
                else:
                    # Если достигнут конец таблицы, возвращаемся к началу
                    select = "SELECT * FROM Customers ORDER BY Контрагент LIMIT 1"
                    cursor.execute(select)
                    row = cursor.fetchone()

                    self.lineE_NumberCustomer.setText(str(row[0]))
                    self.lineE_Name.setText(str(row[1]))
                    self.lineE_ViewCustomer.setText(str(row[2]))
                    self.lineE_Document.setText(str(row[3]))
                    self.lineE_DataDocument.setText(str(row[4]))
                    self.lineE_INN.setText(str(row[5]))
                    self.lineE_KPP.setText(str(row[6]))
                    self.lineE_Requisites.setText(str(row[7]))
                    self.lineE_login.setText(str(row[8]))
                    self.lineE_password.setText(str(row[9]))

                    MessageBox.Message_Info("Вы просмотрели все записи, программа вернет вас в начало!")
            except TypeError:
                MessageBox.Message_Info("Нет данных для отображения")
        except Exception as Error:
            MessageBox.Message_Warning(f"Ошибка: {Error}")

    def Back(self):
        connection = self.connection
        cursor = connection.cursor()
        try:
            number_customer = self.lineE_NumberCustomer.text()

            select = "SELECT * FROM Customers WHERE Контрагент < %s ORDER BY Контрагент DESC LIMIT 1"
            cursor.execute(select, (number_customer,))

            row = cursor.fetchone()

            try:
                if row:
                    # Добавляем данные в LineEdit
                    self.lineE_NumberCustomer.setText(str(row[0]))
                    self.lineE_Name.setText(str(row[1]))
                    self.lineE_ViewCustomer.setText(str(row[2]))
                    self.lineE_Document.setText(str(row[3]))
                    self.lineE_DataDocument.setText(str(row[4]))
                    self.lineE_INN.setText(str(row[5]))
                    self.lineE_KPP.setText(str(row[6]))
                    self.lineE_Requisites.setText(str(row[7]))
                    self.lineE_login.setText(str(row[8]))
                    self.lineE_password.setText(str(row[9]))
                else:
                    MessageBox.Message_Info("Вы находитесь на последней записи")
            except TypeError:
                MessageBox.Message_Info("Нет данных для отображения")
        except Exception as Error:
            MessageBox.Message_Warning(f"Ошибка: {Error}")

    def Delete(self):
        connection = self.connection  # Импортируем соединение
        cursor = connection.cursor()  # Создаем метод курсор

        try:
            # Получаем данные из lineEdit и преобразуем их в int
            data_str = self.lineE_NumberCustomer.text()
            try:
                data = int(data_str)
            except ValueError:
                # Если введенное значение нельзя преобразовать в int, выводим сообщение об ошибке
                MessageBox.Message_Warning("Вы ввели некорректный Номер! Попробуйте снова.")
                return

            if data is not None:
                # Проверяем есть ли заказчик с таким id
                check_query = f"SELECT * FROM customers WHERE Контрагент = {data}"
                cursor.execute(check_query)  # Ищем заказчика с таким id
                result = cursor.fetchone()  # Получаем одну строку результата

                # Если результат был найден
                if result is not None:
                    delete = f"DELETE FROM Customers WHERE Контрагент = {data}"  # Создаем запрос к БД
                    cursor.execute(delete)  # Удаляем данные из таблицы
                    connection.commit()  # Фиксируем изменения
                    MessageBox.Message_Info("Данные о заказчике были успешно удалены из базы данных!")
                    self.Clear()
                else:
                    MessageBox.Message_Warning("Заказчика с таким 'Номером' не существует! Проверьте "
                                               "введенные данные.")
                    return
            else:
                MessageBox.Message_Warning("Вы ввели некорректный Номер! Попробуйте снова")
                return
        except Exception as Error:
            if "1451 (23000)" in str(Error):
                MessageBox.Message_Warning(
                    "Информацию о заказчике нельзя удалить, так как она используется в других таблицах.")
            else:
                MessageBox.Message_Warning(f"Ошибка: {Error}")

    def GoCustomer(self):
        # Передаем данные подключения
        connection = self.connection
        cursor = connection.cursor()
        number_customer = self.lineE_NumberCustomer.text()

        try:
            select = "SELECT Наименование, Вид_контрагента, Идентифицирующий_документ, Данные_документа, ИНН," \
                     "КПП, Банковские_реквизиты, Логин, Пароль FROM Customers WHERE Контрагент = %s"
            cursor.execute(select, (number_customer,))

            customer_data = cursor.fetchone()

            if customer_data:
                # Добавляем данные в LineEdit
                self.lineE_Name.setText(str(customer_data[0]))
                self.lineE_ViewCustomer.setText(str(customer_data[1]))
                self.lineE_Document.setText(str(customer_data[2]))
                self.lineE_DataDocument.setText(str(customer_data[3]))
                self.lineE_INN.setText(str(customer_data[4]))
                self.lineE_KPP.setText(str(customer_data[5]))
                self.lineE_Requisites.setText(str(customer_data[6]))
                self.lineE_login.setText(str(customer_data[7]))
                self.lineE_password.setText(str(customer_data[8]))
                # Обновляем предыдущий ID заказчика
                self.last_number_customer = number_customer
                MessageBox.Message_Info("Данные заказчика были успешно загружены")
            else:
                MessageBox.Message_Info("Заказчик с указанным 'Номером' не найден")
        except Exception as Error:
            MessageBox.Message_Warning(f"Ошибка: {Error}")

    def Correctly(self):
        # Импортируем соединение с БД
        connection = self.connection
        cursor = connection.cursor()

        try:
            # Считываем данные из lineEdit
            number_customer = self.lineE_NumberCustomer.text()

            try:
                int(number_customer)
            except ValueError:
                MessageBox.Message_Warning("Вы ввели некорректное число! Попробуйте снова.")
                return

            # Проверяем существование ID в базе данных
            cursor.execute("SELECT COUNT(*) FROM Customers WHERE Контрагент = %s", (number_customer,))
            if cursor.fetchone()[0] == 0:
                MessageBox.Message_Warning("Записи с указанным 'ИНН' не существует.")
                return

            if number_customer is not None:
                update_query = "UPDATE Customers SET "
                update_values = []
                changes_exist = False  # Переменная для отслеживания наличия изменений

                # Проверяем каждое поле на наличие изменений
                if self.lineE_Name.isModified():
                    update_query += "Наименование = %s, "
                    update_values.append(self.lineE_Name.text())
                    changes_exist = True

                if self.lineE_ViewCustomer.isModified():
                    update_query += "Вид_контрагента = %s, "
                    update_values.append(self.lineE_ViewCustomer.text())
                    changes_exist = True

                if self.lineE_Document.isModified():
                    update_query += "Идентифицирующий_документ = %s, "
                    update_values.append(self.lineE_Document.text())
                    changes_exist = True

                if self.lineE_DataDocument.isModified():
                    update_query += "Данные_документа = %s, "
                    update_values.append(self.lineE_DataDocument.text())
                    changes_exist = True

                if self.lineE_INN.isModified():
                    update_query += "ИНН = %s, "
                    update_values.append(self.lineE_INN.text())
                    changes_exist = True

                if self.lineE_KPP.isModified():
                    update_query += "КПП = %s, "
                    update_values.append(self.lineE_KPP.text())
                    changes_exist = True

                if self.lineE_Requisites.isModified():
                    update_query += "Банковские_реквизиты = %s, "
                    update_values.append(self.lineE_Requisites.text())
                    changes_exist = True

                if self.lineE_login.isModified():
                    update_query += "Логин = %s, "
                    update_values.append(self.lineE_login.text())
                    changes_exist = True

                if self.lineE_password.isModified():
                    update_query += "Пароль = %s "
                    update_values.append(self.lineE_password.text())
                    changes_exist = True

                # Если изменений нет, то выводим сообщение об этом
                if not changes_exist:
                    MessageBox.Message_Info("Данные не были изменены!")
                    return

                update_query += "WHERE Контрагент = %s"
                update_values.append(number_customer)

                # Удаляем лишние запятые в запросе
                update_query = update_query.replace(", WHERE", " WHERE")

                cursor.execute(update_query, update_values)

                MessageBox.Message_Info("Данные были успешно отредактированы!")
            else:
                MessageBox.Message_Warning("Вы ввели некорректные данные! Попробуйте снова.")
                return
        except Exception as Error:
            MessageBox.Message_Warning(f"Ошибка: {Error}")

    def Exit(self):
        try:
            # Закрываем текущую форму
            self.close()

            # Импортируем класс Form_Main только здесь, в момент вызова метода Exit
            from Form_Main_Employee import Form_Main_Employee

            self.form_main_employee = Form_Main_Employee(self.connection)  # Создаем экземпляр класса Form_Main
            self.form_main_employee.show()  # Отображаем Form_Main
        except Exception as Error:
            MessageBox.Message_Warning(f"Ошибка: {Error}")
