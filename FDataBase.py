import psycopg2
from psycopg2.extras import DictCursor
from psycopg2 import sql



# получение всех доступных тренировок из бд
def getTrainingAnounce(db):
    try:
        with db.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute("SELECT * FROM training")
            res = cursor.fetchall()
            if res :
                return res
    except Exception as e:
        print(e)
        print("Ошибка в получении тренировок.")

    return []

# получение всех клиентов из бд
def getClientAnounce(db):
    try:
        with db.cursor(cursor_factory=DictCursor) as cursor:

            cursor.execute("SELECT * FROM client ORDER BY client_number")
            res = cursor.fetchall()
            if res:
                return res
    except Exception as e:
        print(e)
        print("Ошибка в получении клиентов.")

    return []


# поиск клиента по его id
def findClientById(client_id, db):
    try:
        with db.cursor() as cursor:

            cursor.execute("SELECT * FROM client WHERE client_number=%(client_number)s",
                           {'client_number': client_id})
            res = cursor.fetchone()
            if res:
                return res
    except Exception as e:
        print(e)
        print("Ошибка получения клиента по его id.")

    return False

# поиск группы по ее Id
def findGroupById(group_id, db):
    try:
        with db.cursor() as cursor:

            cursor.execute("SELECT * FROM vieww WHERE group_number=%(gr_number)s",
                           {'gr_number': group_id})
            res = cursor.fetchone()
            if res:
                return res
    except Exception as e:
        print(e)
        print("Ошибка получения группы по его id.")

    return False

# добавление новой клиента в бд
def addclient(firstname, surname, lastname, phone, mail, address, date, group, db):
    try:
        with db.cursor() as cursor:
            cursor.execute("ROLLBACK;")
            query1 = sql.SQL("CALL add_client_transaction({fn},{sn},{ln},{ph},{em},{adr},{dt},{grr})") \
                .format(fn=sql.Literal(firstname), sn=sql.Literal(surname), ln=sql.Literal(lastname),
                        ph=sql.Literal(phone), em=sql.Literal(mail), adr=sql.Literal(address),
                        dt=sql.Literal(date), grr=sql.Literal(group))
            cursor.execute(query1)
            db.commit()
    except Exception as e:
        print("Ошибкад добавления клиента." + e)
        return False

    return True


# добавление новой тренировки в бд
def addtrain(start, finish, group, trainer, description,equip, db):
    try:
        with db.cursor() as cursor:
            cursor.execute("ROLLBACK;")
            query1 = sql.SQL("CALL add_training({strt},{fnsh},{descr},{gr},{tr}, {eq})") \
                .format(strt=sql.Literal(start), fnsh=sql.Literal(finish),
                        descr=sql.Literal(description), gr=sql.Literal(group),
                        tr=sql.Literal(trainer),eq=sql.Literal(equip))
            cursor.execute(query1)

    except Exception as e:
        print("Ошибка при добавлении тренировки " + e)
        return False

    return True


# получить тренировки по ее id из бд
def getTrain(id, db):
    try:
        with db.cursor() as cursor:
            cursor.execute("SELECT * FROM training WHERE training_number = %(training_number)s",
                           {'training_number': id})
            res = cursor.fetchone()
            if res:
                return res
    except Exception as e:
        print(e)
        print("Ошибка получения тренировки из БД.")
    return (False, False)

# получение клиента по его Id
def getClient(id, db):
    try:
        with db.cursor() as cursor:
            cursor.execute("SELECT * FROM client WHERE client_number = %(client_number)s",
                           {'client_number': id})
            res = cursor.fetchone()
            if res:
                return res
    except Exception as e:
        print(e)
        print("Ошибка получения клиента из БД.")
    return (False, False)

# обновление данных у клиента
def updateClient(firstn, surn, lastn, phone, email, address, db, id_client):
    try:
        with db.cursor() as cursor:
            query1 = sql.SQL("UPDATE client SET client_firstname = {first},client_surname = {sur},"
                             "client_lastname = {last},client_phone = {ph},client_email = {em},"
                             "client_address = {addr}"
                             "WHERE client_number = {client_num}") \
                .format(first=sql.Literal(firstn), sur=sql.Literal(surn),
                        last=sql.Literal(lastn), ph=sql.Literal(phone),
                        em=sql.Literal(email),addr=sql.Literal(address),
                        client_num=sql.Literal(id_client))
            cursor.execute(query1)
        db.commit()
    except Exception as e:
        print(e)
        print("Ошибка редактирования клиента.")

# добавление спотр. оборудования
def addequipment(name, code, amount, db):
    try:
        with db.cursor() as cursor:
            query1 = sql.SQL("CALL add_equip({nam}, {cod}, {amoun})") \
                .format(nam=sql.Literal(name),cod=sql.Literal(code),amoun=sql.Literal(amount))
            cursor.execute(query1)
        db.commit()
    except Exception as e:
        print(e)
        print("Ошибка добавления спорт. инвентаря.")

# получение спорт. оборудования
def getequip(id,db):
    try:
        with db.cursor() as cursor:
            cursor.execute("SELECT * FROM sport_equipment WHERE sport_equip_number = %(sport_equip_number)s",
                           {'sport_equip_number': id})
            res = cursor.fetchone()
            if res:
                return res
    except Exception as e:
        print(e)
        print("Ошибка получения оборудования по id.")
    return (False, False)

# редактирование спорт. оборудования
def editequipment(name, code, amount,id, db):
    try:
        with db.cursor() as cursor:
            query1 = sql.SQL("UPDATE sport_equipment SET sport_equip_name = {nam},"
                             "sport_equip_vendore_code = {cod},"
                             "sport_equip_amount = {amou}"
                             "WHERE sport_equip_number = {idd}") \
                .format(nam=sql.Literal(name),cod=sql.Literal(code),amou=sql.Literal(amount),
                        idd=sql.Literal(id))
            cursor.execute(query1)
        db.commit()
    except Exception as e:
        print(e)
        print("Ошибка добавления спорт. инвентаря.")

# удаление клиента
def deleteclient(id, db):
    try:
        with db.cursor() as cursor:
            query1 = sql.SQL("CALL delete_client_relationchip({clientnum})") \
                .format(clientnum=sql.Literal(id))
            cursor.execute(query1)
        db.commit()
    except Exception as e:
        print(e)
        print("Ошибка удаления клиента.")

# удаление работника
def deleteEmpl(id,db):
    try:
        with db.cursor() as cursor:
            cursor.execute("SELECT employee_login FROM employee WHERE employee_number = %(empl_n)s",
                            {'empl_n':id})
            log_e = cursor.fetchone()

            query1 = sql.SQL("SELECT delete_employee_and_role({empnum}, {emplog})") \
                .format(empnum=sql.Literal(id), emplog=sql.Literal(log_e))
            cursor.execute(query1)
        db.commit()
    except Exception as e:
        print(e)
        print("Ошибка удаления работника.")

# удаление клиента из группы
def deleteClientFromGr(id_cl,id_gr,db):
    try:
        with db.cursor() as cursor:
            cursor.execute("DELETE FROM client_group_table WHERE client_number = %(cl_n)s AND "
                           "group_number = %(group)s",
                            {'cl_n':id_cl, 'group':id_gr})
        db.commit()
    except Exception as e:
        print(e)
        print("Ошибка удаления клиента из группы.")

# добавление клиента в группу
def insertClientToGr(id_cl,id_gr,db):
    try:
        with db.cursor() as cursor:
            query = sql.SQL("INSERT INTO client_group_table(group_number,client_number) "
                            "VALUES ({gr},{cl});") \
                .format(gr=sql.Literal(id_gr), cl=sql.Literal(id_cl))
            cursor.execute(query)
        db.commit()
    except Exception as e:
        print(e)
        print("Ошибка добавление клиента в группу.")

 # добавление оборудования тренировке
def insertEquipToTr(id_eq,id_tr,db):
    try:
        with db.cursor() as cursor:
            query = sql.SQL("INSERT INTO sport_equip_training(sport_equip_number,training_number) "
                            "VALUES ({eq},{tr});") \
                .format(eq=sql.Literal(id_eq), tr=sql.Literal(id_tr))
            cursor.execute(query)
        db.commit()
    except Exception as e:
        print(e)
        print("Ошибка добавление клиента в группу.")

#  для менеджера и обычного сотрудника запросы на изменение тренировок разные.
def updateTrain(start, finish, group, trainer, description, db, train_id, is_manager, is_admin):
    try:
        with db.cursor() as cursor:
            if is_manager or is_admin:
                query = sql.SQL("UPDATE training SET start_time = {startd},finish_time = {finishd},"
                                "training_name = {descriptions},"
                                "group_number = {groupn},trainer_number = {trainern} "
                                "WHERE training_number = {train_num}") \
                    .format(startd=sql.Literal(start), finishd=sql.Literal(finish),
                            descriptions=sql.Literal(description),
                            groupn=sql.Literal(group), trainern=sql.Literal(trainer),
                            train_num=sql.Literal(train_id))

                cursor.execute(query)
            else:
                query1 = sql.SQL("UPDATE training SET start_time = {startd},finish_time = {finishd}"
                                 "WHERE training_number = {train_num}") \
                    .format(startd=sql.Literal(start), finishd=sql.Literal(finish),
                            train_num=sql.Literal(train_id))
                cursor.execute(query1)
        db.commit()
    except Exception as e:
        print(e)
        print("Ошибка редактирования тренировки.")

# получение view в котором отображается кол-во клиентов в группе и данные группы
def getgroupsview(db):
    try:
        with db.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute("SELECT * FROM vieww;")
            res = cursor.fetchall()
            if not res:
                print("Группы не найдены.")
                return False
            return res
    except Exception as e:
        print(e)
        print("Ошибка получения спорт. групп из бд.")
    return False

# получение данных спорт. оборудования для выбора при создании тренировки
def getequipforchose(db):
    try:
        with db.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute("SELECT * FROM sport_equipment")
            res = cursor.fetchall()
            if not res:
                print("Оборудование не найдено.")
                return False
            return res
    except Exception as e:
        print(e)
        print("Ошибка получения спорт. оборудования из бд.")
    return False

# получение спорт. групп для клиента
def getgroupsforclient(db):
    try:
        with db.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute("SELECT * FROM sports_group")
            res = cursor.fetchall()
            if not res:
                print("Группы не найдены.")
                return False
            return res
    except Exception as e:
        print(e)
        print("Ошибка получения спорт. групп из бд.")
    return False

#получение view в котором отображаются, к каким группам относятся клиенты
def getgroupstable(client_id,db):
    try:
        with db.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute("SELECT * FROM group_client WHERE client_number = %(client_num)s",
                           {'client_num':client_id})
            res = cursor.fetchall()
            if not res:
                print("Группы клиента не найдены.")
                return False
            return res
    except Exception as e:
        print(e)
        print("Ошибка получения спорт. групп клиента из бд.")
    return False

def getequipstable(train_id,db):
    try:
        with db.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute("SELECT * FROM equip_train_view WHERE training_number = %(train_num)s",
                           {'train_num': train_id})
            res = cursor.fetchall()
            if not res:
                print("Оборудование тренировки не найдено.")
                return []
            return res
    except Exception as e:
        print(e)
        print("Ошибка получения спорт. оборудования из бд.")
    return False

# добавление спорт. группы
def addgroup(name, type, db):
    try:
        with db.cursor() as cursor:
            query = sql.SQL("CALL add_group({nam},{typ})") \
                .format(nam=sql.Literal(name), typ=sql.Literal(type))
            cursor.execute(query)
            db.commit()
    except Exception as e:
        print("Ошибка добавления группы" + e)
        return False

    return True


# добавление нового пользователя в бд
def addUser(firstname, surname, lastname, email, phone, login, password, expirience, role, db):
    try:

        # номер роли для процедуры
        id_role = 0
        if role == 'trainer':
            id_role = 2
        if role == 'manager':
            id_role = 1
        with db.cursor() as cursor:
            query = sql.SQL("CALL create_user({fn},{sn},{ln},{em},{ph},{lg},{psw},{exp},{role})") \
                .format(fn=sql.Literal(firstname), sn=sql.Literal(surname), ln=sql.Literal(lastname),
                        em=sql.Literal(email), ph=sql.Literal(phone), lg=sql.Literal(login),
                        psw=sql.Literal(password), exp=sql.Literal(expirience), role=sql.Literal(id_role), )
            cursor.execute(query)
            db.commit()
    except Exception as e:
        print(e)
        print("Ошибка добавления пользователя в бд")
        return False

    return True

# получение спорт. оборудования
def getequips(db):
    try:
        with db.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute("SELECT * FROM sport_equipment")
            res = cursor.fetchall()
            if not res:
                print("Спортивное снаряжение не найдено.")
                return False
            return res
    except Exception as e:
        print(e)
        print("Ошибка получения спотр. снаряжения из бд.")
    return False


# получение пользователя из бд по его Id
def getUser(user_id, db):
    try:
        with db.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute("SELECT * FROM employee WHERE employee_number = %(employee_number)s",
                           {'employee_number': user_id})
            res = cursor.fetchone()
            if not res:
                print("Пользовтель не найден.")
                return False
            return res
    except Exception as e:
        print(e)
        print("Ошибка получения данных из бд.")
    return False


# получение пользователя из бд по его логину
def getUserByLogin(login, db):
    try:
        with db.cursor(cursor_factory=DictCursor) as cursor:
            try:
                cursor.execute("SELECT * FROM employee WHERE employee_login = %(employee_login)s",
                               {'employee_login': login})
                res = cursor.fetchone()
            except psycopg2.OperationalError as e:
                print(e)
                res = False
            # if not res:
            # print("Пользователь не найден.")
            return res

    except Exception as e:
        print(e)
        print("Ошибка получения пользователя из бд.")

    return False


# получение пароля пользователя по его логину
def getPassUserByLogin(login, pasw, db):
    try:
        with db.cursor(cursor_factory=DictCursor) as cursor:
            query = sql.SQL("SELECT employee_password "
                            "FROM employee WHERE employee_login = {logi}") \
                .format(passws=sql.Literal(pasw),
                        logi=sql.Literal(login))

            cursor.execute(query)
            res = cursor.fetchone()[0]
            if not res:
                print("Пользователь не найден.")
                return False
            return res

    except Exception as e:
        print(e)
        print("Ошибка получения пользователя из бд.")

    return False


# получение номера позиции пользователя
def getPositionUser(user_id, db):
    try:
        with db.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute("SELECT position_number FROM employee WHERE employee_number = %(employee_number)s",
                           {'employee_number': user_id})
            res = cursor.fetchone()
            if not res:
                print("Пользователя с таким id нет.")
                return False
            return res

    except Exception as e:
        print(e)
        print("Ошибка получения юзера из бд.")

    return False

# получение названия позиции
def getNamePosition(user_id, db):
    try:
        with db.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute("SELECT * FROM position_emp WHERE position_number = %(employee_number)s",
                           {'employee_number': user_id})
            res = cursor.fetchone()
            if not res:
                print("Позиции с таким id не найдено.")
                return False
            return res

    except Exception as e:
        print(e)
        print("Ошибка получения позиции из бд.")

    return False

# создание отчета по тренировкам
def get_report_task(path, start, finish, db):
    try:
        with db.cursor() as cursor:
            query = sql.SQL("CALL export_data_training_csv({startd},{finishd},{paths})") \
                .format(startd=sql.Literal(start),
                        finishd=sql.Literal(finish),
                        paths=sql.Literal(path))
            cursor.execute(query)

    except Exception as e:
        print(e)
        print("Ошибка вызова функции генерации отчета по сотруднику.")
        return False

    return True
