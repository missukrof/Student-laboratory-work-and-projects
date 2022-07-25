import openpyxl as opx

# База данных .csv -> .xlsx (источник: linis-crowd.org)
records = opx.load_workbook('words_all_full_rating.xlsx', read_only=True)
first_sheet = records.worksheets[0]

estimation_book = {}

for row in first_sheet.rows:
    estimation_book[row[0].value] = row[1].value

print(estimation_book)

estimation_book_1 = {}

with open('estimations_1.txt', 'r', encoding='utf-8') as estimations_1:
    for line in estimations_1:
        try:
            l = line.split()
            estimation_book_1[l[0]] = int(l[1])
        except ValueError:
            estimation_book_1[l[0]] = -1
            continue
        except IndexError:
            continue

print(estimation_book_1)

with open('estimations_01.txt', 'r', encoding='utf-8') as estimations:
    for line in estimations:
        c = 0
        for k, v in estimation_book.items():
            if k == line[:-2]:
                with open('estimations.txt', 'a', encoding='utf-8') as rated_estimations:
                    rated_estimations.write('{} {}\n'.format(line[:-2], v))
                c += 1
                break
        if c != 1:
            c1 = 0
            for k1, v1 in estimation_book_1.items():
                if k1 == line[:-2]:
                    with open('estimations.txt', 'a', encoding='utf-8') as rated_estimations1:
                        rated_estimations1.write('{} {}\n'.format(line[:-2], v1))
                    c1 += 1
                    break
            if c1 != 1:
                with open('estimations.txt', 'a', encoding='utf-8') as rated_estimations2:
                    rated_estimations2.write(line)
