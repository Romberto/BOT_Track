from datetime import datetime
from pprint import pprint

import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials
from data.config import SPREADSHEET_ID
import logging


class SheetDoc:
    def __init__(self):
        # Файл, полученный в Google Developer Console
        CREDENTIALS_FILE = 'creds.json'
        # ID Google Sheets документа (можно взять из его URL)

        # Авторизуемся и получаем service — экземпляр доступа к API
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            CREDENTIALS_FILE,
            ['https://www.googleapis.com/auth/spreadsheets',
             'https://www.googleapis.com/auth/drive'])
        httpAuth = credentials.authorize(httplib2.Http())
        service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)
        self.service = service
        self.spreadsheet_id = SPREADSHEET_ID

    # возвращает данные задданного диапозона таблицы
    # ss.get_value('A2:D30')
    # return
    # [['12.06.2023', '475, 843', '1200', 'неопл'],
    #  ['13.06', '77', '1000', 'неопл'],
    #  [],
    #  [],
    #  [],
    #  [],
    #  ['ИТОГО:', '', '2200']]
    async def get_all_value(self):
        target_value = 'ИТОГО:'

        # Запрос на получение значений из таблицы
        sheet = self.service.spreadsheets()
        result = sheet.values().get(spreadsheetId=self.spreadsheet_id, range=f'Лист1!A1:ZZ').execute()
        values = result.get('values', [])

        row_number = None
        for i, row in enumerate(values):

            if len(row) > 0 and row[0] == target_value:
                row_number = i + 1  # Строки в таблице нумеруются с 1
                break

        values = self.service.spreadsheets().values().get(
            spreadsheetId=self.spreadsheet_id,
            range=f'A2:E{row_number}',
            majorDimension='ROWS'
        ).execute()

        return values['values']

    # статус оплачено всегда в столбце D , принимает номер строки : str
    # меняет статус на противоположный
    async def toggle_status(self, row_number):
        values = self.service.spreadsheets().values().get(
            spreadsheetId=self.spreadsheet_id,
            range=f'E{row_number}:E{row_number}',
            majorDimension='ROWS'
        ).execute()
        status = values['values'][0][0]

        if status == 'неопл':
            requests = [
                {
                    'updateCells': {
                        'rows': [
                            {
                                'values': [
                                    {
                                        'userEnteredFormat': {
                                            'backgroundColor': {
                                                'red': 0.0,
                                                'green': 1.0,
                                                'blue': 0.0,
                                                'alpha': 1.0
                                            }
                                        }
                                    }
                                ]
                            }
                        ],
                        'fields': 'userEnteredFormat.backgroundColor',
                        'start': {
                            'sheetId': 0,
                            'rowIndex': (int(row_number) - 1),  # Номер строки (начиная с 0)
                            'columnIndex': 4  # Номер столбца (начиная с 0)
                        }
                    }
                },
                {
                    'pasteData': {
                        'data':'опл',
                        'type': 'PASTE_NORMAL',
                        'delimiter': ',',
                        'coordinate': {
                            'sheetId': 0,
                            'rowIndex': int(row_number-1),
                            'columnIndex': 4
                        }
                    }
                }
            ]
            self.service.spreadsheets().batchUpdate(spreadsheetId=self.spreadsheet_id,
                                                    body={'requests': requests}).execute()
            # values = [
            #     ['опл']
            # ]
            # body = {'values': values}
            # # Отправка запроса на изменение данных в ячейке
            # self.service.spreadsheets().values().update(
            #     spreadsheetId=self.spreadsheet_id,
            #     range=f'Лист1!E{row_number}',
            #     valueInputOption='USER_ENTERED',
            #     body=body
            # ).execute()

        else:
            logging.info('статус не определён')
            print('статус не определён')

    # prefix='all' все доставки
    # prefix='pay' оплаченные доставки
    # prefix='no_pay' не оплаченные доставки

    async def get_track(self, prefix):
        all_data = await self.get_all_value()

        count = 0
        summ = 0
        result = []
        if prefix == 'all':
            for item in all_data:

                if len(item) == 5:
                    count += 1
                    summ += int(item[-3])

        elif prefix == 'pay':

            for item in all_data:

                if len(item) == 5 and item[-1] == 'опл':

                    count += 1
                    summ += int(item[-3])

        elif prefix == 'no_pay':

            row = 1
            for item in all_data:
                row += 1
                if len(item) == 5 and item[-1] == 'неопл':
                    count += 1
                    summ += (int(item[-2])+ int(item[-3]))
                    result.append({row: (int(item[-2])+ int(item[-3]))})

        return {'count': count, 'summ': summ, 'rows': result}

    async def get_row(self, number_row: int):
        sheet = self.service.spreadsheets()
        result = sheet.values().get(spreadsheetId=self.spreadsheet_id,
                                    range=f'Лист1!A{number_row}:D{number_row}').execute()
        values = result.get('values', [])
        return values[0]

    async def add_row(self, quantity_cars:int,summ_azs:int):
        # Запрос на получение информации о таблице
        result = self.service.spreadsheets().values().get(spreadsheetId=self.spreadsheet_id,
                                                          range=f'Лист1!A1:ZZ').execute()
        values = result.get('values', [])
        last_row = int(len(values))
        date = datetime.today().strftime('%d.%m')
        summ_azs = quantity_cars*100

        new_row_data = [date, str(quantity_cars), '1000', str(summ_azs) ,'неопл']
        itog = ['ИТОГО:', '', f'=SUM(C2:C{str(last_row)})', '']
        requests = [
            {
                'insertRange': {
                    'range': {
                        'sheetId': 0,
                        'startRowIndex': last_row - 1,
                        'endRowIndex': last_row
                    },
                    'shiftDimension': 'ROWS'
                }
            },
            {
                'updateCells': {
                    'rows': [
                        {
                            'values': [
                                {
                                    'userEnteredFormat': {
                                        'backgroundColor': {
                                            'red': 1.0,
                                            'green': 1.0,
                                            'blue': 1.0,
                                            'alpha': 1.0
                                        }
                                    }
                                }
                            ]
                        }
                    ],
                    'fields': 'userEnteredFormat.backgroundColor',
                    'range': {
                        "sheetId": 0,
                        "startRowIndex": last_row - 1,
                        "endRowIndex": last_row,
                        "startColumnIndex": 0,
                        "endColumnIndex": 4
                    }

                }
            },
            {
                'updateCells': {
                    'rows': [
                        {
                            'values': [
                                {
                                    'userEnteredFormat': {
                                        'backgroundColor': {
                                            'red': 1.0,
                                            'green': 0.0,
                                            'blue': 0.0,
                                            'alpha': 0.0
                                        }
                                    }
                                }
                            ]
                        }
                    ],
                    'fields': 'userEnteredFormat.backgroundColor',
                    'range': {
                        "sheetId": 0,
                        "startRowIndex": last_row - 1,
                        "endRowIndex": last_row,
                        "startColumnIndex": 4,
                        "endColumnIndex": 5
                    }

                }
            },
            {
                'updateCells': {
                    'rows': [
                        {
                            'values': [
                                {
                                    'userEnteredFormat': {
                                        'backgroundColor': {
                                            'red': 1.0,
                                            'green': 1.0,
                                            'blue': 0.0,
                                            'alpha': 0.0
                                        }
                                    }
                                }
                            ]
                        }
                    ],
                    'fields': 'userEnteredFormat.backgroundColor',
                    'range': {
                        "sheetId": 0,
                        "startRowIndex": last_row - 1,
                        "endRowIndex": last_row,
                        "startColumnIndex": 0,
                        "endColumnIndex": 1
                    }

                }
            },
            {
                'pasteData': {
                    'data': ','.join(new_row_data),
                    'type': 'PASTE_NORMAL',
                    'delimiter': ',',
                    'coordinate': {
                        'sheetId': 0,
                        'rowIndex': last_row - 1,
                        'columnIndex': 0
                    }
                }
            },
            {
                'pasteData': {
                    'data': ','.join(itog),
                    'type': 'PASTE_NORMAL',
                    'delimiter': ',',
                    'coordinate': {
                        'sheetId': 0,
                        'rowIndex': last_row,
                        'columnIndex': 0
                    }
                }
            }

        ]

        # Отправка запроса на вставку строки
        self.service.spreadsheets().batchUpdate(spreadsheetId=self.spreadsheet_id,
                                                body={'requests': requests}).execute()
        return len(values)

    


if __name__ == '__main__':
    pass
