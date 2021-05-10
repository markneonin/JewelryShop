from datetime import datetime
from django.conf import settings
from rest_framework.exceptions import ParseError
from rest_framework_csv.orderedrows import OrderedRows
from rest_framework_csv.parsers import CSVParser, universal_newlines, unicode_csv_reader


class Parser(CSVParser):

    def validate(self, row, index):
        if len(row) != 5:
            raise ParseError(f'Ошибка в строке {index}: неверное кол-во элементов')

        customer_name = row[0]

        gem_name = row[1].lower()

        try:
            amount = int(row[2])
            if amount < 1 or amount > 10**18:
                raise ParseError(f'Ошибка в строке {index}: сумма сделки должна быть положительным числом меньшим 10^18')
        except ValueError:
            raise ParseError(f'Ошибка в строке {index}: сумма сделки должна быть представлена числом')

        try:
            quantity = int(row[3])
            if quantity < 1 or amount > 10**18:
                raise ParseError(f'Ошибка в строке {index}: кол-во товаров должно быть положительным числом меньшим '
                                 f'10^18')
        except ValueError:
            raise ParseError(f'Ошибка в строке {index}: кол-во товаров должно быть представлено числом')

        try:
            date = datetime.strptime(row[4], '%Y-%m-%d %H:%M:%S.%f')
        except ValueError:
            raise ParseError(f'Ошибка в строке {index}: неверный формат времени')

        deal = {
            'customer': customer_name,
            'gem': gem_name,
            'date': date,
            'amount': amount,
            'quantity': quantity
        }

        return customer_name, gem_name, deal

    def parse(self, stream):
        delimiter = ','
        encoding = settings.DEFAULT_CHARSET

        try:
            strdata = stream.read()
            binary = universal_newlines(strdata)
            rows = unicode_csv_reader(binary, delimiter=delimiter, charset=encoding)
            data = OrderedRows(next(rows))
            if data.header != ['customer', 'item', 'total', 'quantity', 'date']:
                raise ParseError('Некорректные заголовки файла')

            deals = []
            customers = set()
            gems = set()
            for index, row in enumerate(rows):
                customer_name, gem_name, deal = self.validate(row, index+2)
                deals.append(deal)
                customers.add(customer_name)
                gems.add(gem_name)

            return customers, gems, deals

        except Exception as exc:
            raise ParseError(f'Ошибка валидации CSV - {exc}')


def create_inexistent_items(items, Model):

    existed_items = Model.objects.all()
    output = {}

    for item in existed_items:
        if item.name in items:
            output[item.name] = item
            items.remove(item.name)

    items_obj = [Model(name=i) for i in items]

    created = Model.objects.bulk_create(items_obj)

    for obj in created:
        output[obj.name] = obj

    return output

