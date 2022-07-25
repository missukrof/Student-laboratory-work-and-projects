import string
import datetime

file = open('phone book.txt', 'r', encoding='utf-8')
People = {}
PhoneBook1 = {}


# Сортировка исходного файла по алфавиту (для удобства восприятия, особенно при выводе полного справочника):
def MakeDict():
    def FileSort():
        file = open('phone book.txt', 'r', encoding='utf-8')
        lines = file.readlines()
        lines = [line.rstrip('\n') for line in lines]
        lines.sort()
        with open('phone book.txt', 'w') as outfile:
            i = 0
            while i < len(lines) - 1:
                outfile.write(lines[i] + '\n')
                i += 1
            if i == len(lines) - 1:
                outfile.write(lines[i])


    FileSort()
    file = open('phone book.txt', 'r', encoding='utf-8')
    i = 1

    for line in file:
        if len(line.split()) == 0:
            continue
        else:
            (name, surname, date, phone) = line.split()
            People['name'] = name
            People['surname'] = surname
            People['date'] = date
            People['phone'] = phone
            PhoneBook1[i] = People.copy()
            i += 1
    return PhoneBook1


MakeDict()


def ValueCheck(id):  # Проверка уникального идентификатора на содержание только букв, цифр и дефисов
    allowed = string.ascii_letters + string.digits + '-'
    return all(c in allowed for c in id)


def NameCheck():  # Проверка имени на корректность
    enter_name = (input('\tName: ').title())
    if ValueCheck(enter_name):
        return enter_name
    else:
        print('The name contains invalid symbols. Please use the alphabet (a-z, A-Z), numbers or hyphen.')
    return NameCheck()


def SurnameCheck():  # Проверка фамилии на корректность
    enter_surname = (input('\tSurname: ').title())
    if ValueCheck(enter_surname):
        return enter_surname
    else:
        print('The surname contains invalid symbols. Please use the alphabet (a-z, A-Z), numbers or hyphen.')
    return SurnameCheck()


def DateCheck():  # Проверка на фактическое существование даты, на непревышение текущей даты + ввод
    enter_date = input('\tDate of birth (DD.MM.YYYY): ')
    if enter_date == '-':
        enter_date = '---'
        return enter_date
    else:
        try:
            date1 = list(reversed(enter_date.split('.')))
            y = int(date1[0])
            m = int(date1[1])
            d = int(date1[2])
            import datetime
            correctDate = None
            try:
                newDate = datetime.datetime(y, m, d)
                correctDate = True
            except ValueError:
                correctDate = False
            if str(correctDate) == 'True':
                from datetime import datetime
                d1 = datetime.today().strftime('%Y-%m-%d').split('-')
                if len(date1) != len(d1):
                    print('Oops, something went wrong! '
                          'Please enter correct date of birth in format DD.MM.YYYY.')
                    return DateCheck()
                else:
                    if int(date1[0]) == int(d1[0]):
                        if int(date1[1]) == int(d1[1]):
                            if int(date1[2]) <= int(d1[2]):
                                return enter_date
                            else:
                                print('This day will only come soon. '
                                      'Please enter correct date of birth in format DD.MM.YYYY.')
                                return DateCheck()
                        elif int(date1[1]) < int(d1[1]):
                            return enter_date
                        else:
                            print('This month hasn’t come yet!'
                                  ' Please enter correct date of birth in format DD.MM.YYYY.')
                            return DateCheck()
                    elif 1869 < int(date1[0]) < int(d1[0]):
                            return enter_date
                    elif int(date1[0]) > int(d1[0]):
                        print('This year hasn’t come yet!'
                              ' Please enter correct date of birth in format DD.MM.YYYY.')
                        return DateCheck()
                    else:
                        print('Too distant year of birth.'
                              ' I’m afraid, the person has already died...')
                        return DateCheck()
            else:
                print('Such date doesn’t exist.'
                      ' Please enter correct date of birth or enter "-" to leave the gap blank.')
                return DateCheck()
        except ValueError:
            print('Oops, something went wrong!'
                  ' Please enter correct date of birth in format DD.MM.YYYY.')
            return DateCheck()
        except IndexError:
            print('Oops, something went wrong!'
                  ' Please enter correct date of birth in format DD.MM.YYYY.')
            return DateCheck()


def PhoneCheck():  # Проверка номера телефона, автозамена + ввод
    enter_phone = input('\tPhone number: ')
    phone_check = list(enter_phone)
    try:
        if '+' in phone_check:
            phone_check.remove('+')
        if phone_check[0] == '7':
            phone_check[0] = '8'
        enter_phone1 = ''.join(phone_check)
        if not all(c in string.digits for c in enter_phone1) or len(phone_check) != 11:
            print('The phone number must contain 11 digits and'
                  ' should be written in XXXXXXXXXXX format. Please try again.')
            return PhoneCheck()
        else:
            return enter_phone1
    except IndexError:
        print('The phone number must contain 11 digits and'
              ' should be written in XXXXXXXXXXX format. Please try again.')
        return PhoneCheck()
    except ValueError:
        print('The phone number must contain 11 digits and'
              ' should be written in XXXXXXXXXXX format. Please try again.')
        return PhoneCheck()


def Reiteration(operation):  # Запрос на повторение операции
    while True:
        repeat_query = input('Try again? (Please write "yes" or "no")\n').lower()
        if repeat_query in ('y', 'yes', 'yeah', 'yep'):
            return operation()
        elif repeat_query in ('n', 'no', 'nop', 'nope'):
            return None
        print('Oops, something went wrong! Write "yes" or "no", please.')


def DeleteOneRecord(v):  # Удаление одной определённой записи файла
    while True:
        command_phrase1 = input('Please, write "yes" to delete the entry or '
                                '"no" to return to the main menu: ').lower()
        if command_phrase1 in ('y', 'yes', 'yeah', 'yep'):
            with open('phone book.txt', 'r') as f:
                old_record = f.readlines()

            with open('phone book.txt', 'w') as f:
                for line in old_record:
                    if line.strip("\n") != '{} {} {} {}'.format(*v.values()):
                        f.write(line)

            MakeDict()

            print('The record was successfully deleted!')
            return None
        elif command_phrase1 in ('n', 'no', 'nop', 'nope'):
            return None
        print('Oops, something went wrong! Write "yes" or "no", please.')


# Просмотр всех записей справочника:
def PhoneBookView():
    MakeDict()
    print('{name:10}\t\t\t{surname:10}\t\t\t{date:10}\t\t\t{phone:10}'.format(name='Name',
                                                                              surname='Surname',
                                                                              date='Date',
                                                                              phone='Phone number'))
    for k, v in PhoneBook1.items():
        print('{name:10}\t\t\t{surname:10}\t\t\t{date:10}\t\t\t{phone:11}'.format(**v))
    return None


# Поиск по справочнику:
def PhoneBookSearch():
    print('Please complete in all the required forms to search by specific values '
          '(or leave them blank, just press "Enter" to go to the next category).')
    query_name = input('\tName: ').title()
    query_surname = input('\tSurname: ').title()
    query_date = input('\tDate (in format DD.MM or DD.MM.YYYY): ')
    query_phone = input('\tPhone number (in format XXXXXXXXXXX): ')
    founded_records = 0
    if query_name in ('', '-', '.', ',', ' ') and query_surname in ('', '-', '.', ',', ' ') \
            and query_date in ('', '-', '.', ',', ' ') and query_phone in ('', '-', '.', ',', ' '):
        print('You have left all the gaps blank.')
        Reiteration(PhoneBookSearch)
        return None
    for k, v in PhoneBook1.items():
        if query_name in (v.get('name'), '', '-', '.', ',', ' '):
            if query_surname in (v.get('surname'), '', '-', '.', ',', ' '):
                try:
                    date = list(v.get('date').split('.'))
                    day_month = date[0] + '.' + date[1]
                    if query_date in (day_month, '', '-', '.', ',', ' ') or query_date == v.get('date'):
                        if query_phone in (v.get('phone'), '', '-', '.', ',', ' '):
                            print('{name:10}\t\t\t{surname:10}\t\t\t{date:10}\t\t\t{phone:11}'.format(**v))
                            founded_records += 1
                            continue
                except IndexError:
                    if query_date in ('', '-', '.', ',', ' ', '---'):
                        if query_phone in (v.get('phone'), '', '-', '.', ',', ' '):
                            print('{name:10}\t\t\t{surname:10}\t\t\t{date:10}\t\t\t{phone:11}'.format(**v))
                            founded_records += 1
                            continue
    if founded_records == 0:
        print('There’s no records for entered values. Check the entered data and try again.')
        Reiteration(PhoneBookSearch)


# Добавление новой записи в справочник:
def PhoneBookAdd():
    query = input('Please enter a unique identifier (Name Surname) of the new record: ').title()
    q = query.split()
    founded_records = 0
    if len(q) == 2:
        if ValueCheck(q[0]) and ValueCheck(q[1]):
            for k, v in PhoneBook1.items():
                if q[0] in (v.get('name'), '', '-'):
                    if q[1] in (v.get('surname'), '', '-'):
                        founded_records += 1
                        print('A record with the same name already exists: \t{} {} ({}, {})'.format(*v.values()))
                        print('Do you want to:')
                        print('\t1. Edit existing record?')
                        print('\t2. Change the unique identifier (name and surname)?')
                        print('\t3. Return to the main menu?')
                        while True:
                            command_phrase1 = input('Enter your choice: ')
                            if command_phrase1 in ('1', '1.'):
                                with open('phone book.txt', 'r') as f:
                                    old_record = f.readlines()

                                with open('phone book.txt', 'w') as f:
                                    for line in old_record:
                                        if line.strip("\n") != '{} {} {} {}'.format(*v.values()):
                                            f.write(line)

                                print('You can press "Enter" if you don’t want to change the unique identifier.')
                                if NameCheck() in ('', ' ', '-', ','):
                                    v.update((k, q[0]) for k, v in v.items() if v == q[0])
                                else:
                                    v.update((k, NameCheck()) for k, v in v.items() if v == q[0])

                                if SurnameCheck() in ('', ' ', '-', ','):
                                    v.update((k, q[1]) for k, v in v.items() if v == q[1])
                                else:
                                    v.update((k, SurnameCheck()) for k, v in v.items() if v == q[1])

                                v.update((k, DateCheck()) for k, v in v.items() if k == 'date')
                                v.update((k, PhoneCheck()) for k, v in v.items() if k == 'phone')

                                with open('phone book.txt', 'a', encoding='utf-8') as f:
                                    f.writelines('\n{} {} {} {}'.format(*v.values()))

                                print('The record was successfully changed!')
                                return None
                            elif command_phrase1 in ('2', '2.'):
                                return PhoneBookAdd()

                            elif command_phrase1 in ('3', '3.'):
                                return None

                            print('Oops, something went wrong! Please choose the number from 1 to 3.')
            if founded_records == 0:
                print('Please fill all the gaps below:')

                while True:
                    People['name'] = q[0]
                    if ValueCheck(q[0]) not in ('', ' ', '-', ','):
                        print('\tName:', q[0])
                        break
                    print('You should write the name in a correct form.')
                while True:
                    People['surname'] = q[1]
                    if ValueCheck(q[1]) not in ('', ' ', '-', ','):
                        print('\tSurname:', q[1])
                        break
                    print('You should write the surname in a correct form.')

                print('(If you want to leave the next gap blank, enter "-".)')
                People['date'] = DateCheck()
                People['phone'] = PhoneCheck()
                with open('phone book.txt', 'a', encoding='utf-8') as f:
                    f.writelines('\n{} {} {} {}'.format(*People.values()))
                MakeDict()
                print('The new record was successfully added!')
        else:
            print('You should write a unique identifier (Name Surname) in a correct form.')
            return PhoneBookAdd()
    else:
        print('You should write a unique identifier (Name Surname).')
        Reiteration(PhoneBookAdd)


# Удаление записи справочника по уникальному идентификатору или по номеру телефона:
def PhoneBookDelete():
    print('Do you want to delete a record:')
    print('\t1. By the unique identifier (Name Surname)?')
    print('\t2. By the phone number?')
    MakeDict()
    while True:
        command_phrase1 = input('Enter the number ("1" or "2") here (or press "0" to return the main menu): ')
        if command_phrase1 in ('1', '1.'):
            while True:
                query = input('Please enter a unique identifier (Name Surname) for the record to be deleted: ').title()
                print('You should write a unique identifier (Name Surname).')
                q = query.split()
                founded_records = 0
                if len(q) == 2:
                    for k, v in PhoneBook1.items():
                        if q[0] in (v.get('name'), '', '-'):
                            if q[1] in (v.get('surname'), '', '-'):
                                founded_records += 1
                                print('Do you want to delete this phone book record? \t{} {} ({}, {})'.format(*v.values()))
                                DeleteOneRecord(v)
                                return None
                    if founded_records == 0:
                        print('There’re no records for entered values.')
                        Reiteration(PhoneBookDelete)
                        return None
        elif command_phrase1 in ('2', '2.'):
            phone_number = PhoneCheck()
            founded_records = 0
            FoundedRecords = {}
            for k, v in PhoneBook1.items():
                if phone_number in v.get('phone'):
                    founded_records += 1
                    FoundedRecords[founded_records] = dict(v.items())
                    print('{}.\t{} {} ({}, {})'.format(founded_records, *v.values()))
                    continue

            if founded_records == 1:
                for value in FoundedRecords.values():
                    DeleteOneRecord(value)
                    return None

            elif founded_records >= 2:
                while True:
                    try:
                        record_number = int(input('Please select the sequence number of the record you want to delete: '))
                        for key, value in FoundedRecords.items():
                            if key == record_number:
                                value = FoundedRecords.get(key)
                                DeleteOneRecord(value)
                                return None
                    except ValueError:
                        print('Oops, something went wrong! Enter the number of the found record.')

            elif founded_records == 0:
                print('There’re no records for entered values.')
                Reiteration(PhoneBookDelete)
                return None
        elif command_phrase1 in ('0', '0.'):
            return None
        print('Unidentified operation! Choose the number "1" or "2" to perform an operation'
              ' or "0" to return to the main menu.')


# Изменение определённого поля справочника:
def PhoneBookChange():
    query = input('Please enter a unique identifier (Name Surname) for the record: ').title()
    q = query.split()
    founded_records = 0
    MakeDict()
    if len(q) == 2:
        for k, v in PhoneBook1.items():
            if q[0] in (v.get('name'), '', '-'):
                if q[1] in (v.get('surname'), '', '-'):
                    founded_records += 1
                    print('The record has been found: \t{} {} ({}, {})'.format(*v.values()))
                    print('Please select the value you want to change (or press "0" to return the main menu):')
                    print('\t1. Name;')
                    print('\t2. Surname;')
                    print('\t3. Date;')
                    print('\t4. Phone number.')
                    while True:
                        command_phrase1 = input('Enter your choice: ')
                        if command_phrase1 in ('1', '1.'):
                            with open('phone book.txt', 'r') as f:
                                old_record = f.readlines()

                            with open('phone book.txt', 'w') as f:
                                for line in old_record:
                                    if line.strip("\n") != '{} {} {} {}'.format(*v.values()):
                                        f.write(line)

                            if NameCheck() in ('', ' ', '-', ','):
                                v.update((k, q[0]) for k, v in v.items() if v == q[0])
                            else:
                                v.update((k, NameCheck()) for k, v in v.items() if v == q[0])

                            with open('phone book.txt', 'a', encoding='utf-8') as f:
                                f.writelines('\n{} {} {} {}'.format(*v.values()))

                            print('The name was successfully changed!')
                            return None
                        elif command_phrase1 in ('2', '2.'):
                            with open('phone book.txt', 'r') as f:
                                old_record = f.readlines()

                            with open('phone book.txt', 'w') as f:
                                for line in old_record:
                                    if line.strip("\n") != '{} {} {} {}'.format(*v.values()):
                                        f.write(line)

                            if SurnameCheck() in ('', ' ', '-', ','):
                                v.update((k, q[1]) for k, v in v.items() if v == q[1])
                            else:
                                v.update((k, SurnameCheck()) for k, v in v.items() if v == q[1])

                            with open('phone book.txt', 'a', encoding='utf-8') as f:
                                f.writelines('\n{} {} {} {}'.format(*v.values()))

                            print('The surname was successfully changed!')
                            return None
                        elif command_phrase1 in ('3', '3.'):
                            with open('phone book.txt', 'r') as f:
                                old_record = f.readlines()

                            with open('phone book.txt', 'w') as f:
                                for line in old_record:
                                    if line.strip("\n") != '{} {} {} {}'.format(*v.values()):
                                        f.write(line)

                                v.update((k, DateCheck()) for k, v in v.items() if k == 'date')

                            with open('phone book.txt', 'a', encoding='utf-8') as f:
                                f.writelines('\n{} {} {} {}'.format(*v.values()))

                            print('The date of birth was successfully changed!')
                            return None
                        elif command_phrase1 in ('4', '4.'):
                            with open('phone book.txt', 'r') as f:
                                old_record = f.readlines()

                            with open('phone book.txt', 'w') as f:
                                for line in old_record:
                                    if line.strip("\n") != '{} {} {} {}'.format(*v.values()):
                                        f.write(line)

                            v.update((k, PhoneCheck()) for k, v in v.items() if k == 'phone')

                            with open('phone book.txt', 'a', encoding='utf-8') as f:
                                f.writelines('\n{} {} {} {}'.format(*v.values()))

                            print('The phone number was successfully changed!')
                            return None
                        elif command_phrase1 in ('0', '0.'):
                            return None
                        print('Unidentified operation! Choose the number from 1 to 4'
                              ' to perform an operation or 0 to return to the main menu.')
        if founded_records == 0:
            print('There’re no records for entered values.')
            Reiteration(PhoneBookChange)
    else:
        print('You should write a unique identifier (Name Surname).')
        Reiteration(PhoneBookChange)


# Узнать текущий возраст человека:
def PhoneBookAge():
    query = input('Please enter a unique identifier (Name Surname) for the record: ').title()
    q = query.split()
    founded_records = 0
    MakeDict()
    if len(q) == 2:
        for k, v in PhoneBook1.items():
            if q[0] in (v.get('name'), '', '-'):
                if q[1] in (v.get('surname'), '', '-'):
                    founded_records += 1
                    if v.get('date') == '---':
                        print('No birthday data of {} {}.'.format(v.get('name'), v.get('surname')))
                        while True:
                            repeat_query = input('Try again? (Please write "yes" or "no")\n').lower()
                            if repeat_query in ('y', 'yes', 'yeah', 'yep'):
                                return PhoneBookAge()
                            elif repeat_query in ('n', 'no', 'nop', 'nope'):
                                return None
                            print('Oops, something went wrong! Write "yes" or "no", please.')
                    else:
                        from datetime import datetime
                        date_today = datetime.today().strftime('%Y-%m-%d').split('-')
                        date_of_birth = list(reversed(v.get('date').split('.')))
                        if int(date_today[0]) == int(date_of_birth[0]):
                            if int(date_today[1]) == int(date_of_birth[1]):
                                age = int(date_today[2]) - int(date_of_birth[2])
                                print('{} {} is {} days old (date of birthday: {}).'
                                      .format(v.get('name'), v.get('surname'), age, v.get('date')))
                                break
                            else:
                                age = int(date_today[1]) - int(date_of_birth[1])
                                print('{} {} is {} month old (date of birthday: {}).'
                                      .format(v.get('name'), v.get('surname'), age, v.get('date')))
                                break
                        elif int(date_today[1]) > int(date_of_birth[1]):
                            age = int(date_today[0]) - int(date_of_birth[0])
                            print(
                                '{} {} is {} years old (date of birthday: {}).'
                                    .format(v.get('name'), v.get('surname'), age, v.get('date')))
                            break
                        elif int(date_today[1]) == int(date_of_birth[1]):
                            if int(date_today[2]) >= int(date_of_birth[2]):
                                age = int(date_today[0]) - int(date_of_birth[0])
                            else:
                                age = int(date_today[0]) - int(date_of_birth[0]) - 1
                            print(
                                '{} {} is {} years old (date of birthday: {}).'
                                    .format(v.get('name'), v.get('surname'), age, v.get('date')))
                            break
                        elif int(date_today[1]) < int(date_of_birth[1]):
                            age = int(date_today[0]) - int(date_of_birth[0]) - 1
                            print(
                                '{} {} is {} years old (date of birthday: {}).'
                                    .format(v.get('name'), v.get('surname'), age, v.get('date')))
                            break
        if founded_records == 0:
            print('There’re no records for entered values.')
            Reiteration(PhoneBookAge)
    else:
        print('You should write a unique identifier (Name Surname).')
        Reiteration(PhoneBookAge)

# Ближайшие (в диапазоне 30 дней) дни рождения:
def NextBirthdays():
    date_today = datetime.datetime.now()
    date_today1 = date_today.strftime('%d.%m.%Y').split('.')
    days_delta = datetime.timedelta(days=30)
    n_month = (date_today + days_delta).strftime('%d.%m.%Y').split('.')
    MakeDict()
    founded_records = 0
    for v in PhoneBook1.values():
        b_day = list(v.get('date').split('.'))
        if v.get('date') == '---':
            continue
        if b_day[1] == date_today1[1]:
            if b_day[0] >= date_today1[0]:
                print('{name:10} {surname:10}'.format(**v))
                founded_records += 1
        elif b_day[1] == n_month[1]:
            if b_day[0] <= n_month[0]:
                founded_records += 1
                print('{name:10} {surname:10}'.format(**v))
    if founded_records == 0:
        print('There’re no birthdays in the next 30 days.')
    return None


# Начальное приветствие:
def Welcome():
    from datetime import datetime
    now = datetime.now()

    daytime = 'night' if now.hour >= 23 or now.hour < 6 \
        else 'morning' if 6 <= now.hour < 12 \
        else 'afternoon' if 12 <= now.hour < 18 \
        else 'evening'

    print('Good {}!'.format(daytime))


Welcome()
print('Please choose the number from the list of available operations:')
print('\t1. View all phone book records.')
print('\t2. Searching for the specified value.')
print('\t3. Add a new record.')
print('\t4. Delete an existing record.')
print('\t5. Change any box in a specific directory entry.')
print('\t6. Find out a person’s age.')
print('\t7. Find birthdays in the coming month (in the range of 30 days).')

command_phrase = input('Your number: ').lower()

while command_phrase != 'bye':
    if command_phrase in ('1', '1.'):
        PhoneBookView()
        command_phrase = input('You can select another number or end the program by entering "bye": ')
    elif command_phrase in ('2', '2.'):
        PhoneBookSearch()
        command_phrase = input('Please enter the next number from the list of available operations: ')
    elif command_phrase in ('3', '3.'):
        PhoneBookAdd()
        command_phrase = input('Your number: ')
    elif command_phrase in ('4', '4.'):
        PhoneBookDelete()
        command_phrase = input('You can select another number or end the program by entering "bye": ')
    elif command_phrase in ('5', '5.'):
        PhoneBookChange()
        command_phrase = input('Please enter the next number from the list of available operations: ')
    elif command_phrase in ('6', '6.'):
        PhoneBookAge()
        command_phrase = input('Your number: ')
    elif command_phrase in ('7', '7.'):
        NextBirthdays()
        command_phrase = input('You can select another number or end the program by entering "bye": ')
    else:
        print('Oops, something went wrong! '
              'Please choose the number from 1 to 6 or write "bye" to finish the program.')
        command_phrase = input()
print('Hope to see you soon! Bye!')
