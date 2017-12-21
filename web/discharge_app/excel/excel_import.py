import xlrd
import json


def discharge_excel_to_json(filename):
    book = xlrd.open_workbook(filename)

    sh = book.sheet_by_index(0)

    action_date_index = 0
    document_id_index = 0
    debet_index = 0
    credit_index = 0
    name_index = 0

    inn_index = 0

    data = []
    for i, rx in enumerate(range(sh.nrows)):
        if i == 10:
            for index, row in enumerate(sh.row(rx)):
                if row.value == 'Дата операции':
                    action_date_index = index
                elif row.value == 'Номер документа':
                    document_id_index = index
                elif row.value == 'Дебет':
                    debet_index = index
                elif row.value == 'Кредит':
                    credit_index = index
        if i == 11:
            for index, row in enumerate(sh.row(rx)):
                if row.value == 'Наименование ':
                    name_index = index
                if row.value == 'ИНН ':
                    inn_index = index
        if i >= 12:
            d = {
                'action_date': sh.row(rx)[action_date_index].value,
                'document_id': int(sh.row(rx)[document_id_index].value),
                'name': sh.row(rx)[name_index].value,
                'credit': sh.row(rx)[credit_index].value,
                'debet': sh.row(rx)[debet_index].value,
                'inn': sh.row(rx)[inn_index].value
            }
            if d['credit'] == '':
                d['credit'] = 0
            if d['debet'] == '':
                d['debet'] = 0

            data.append(d)
    return json.dumps(data)
