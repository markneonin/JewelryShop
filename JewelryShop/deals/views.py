from .models import Customer, Gem, Deal
from .utils import Parser, create_inexistent_items

from django.db.models import Sum
from rest_framework import viewsets, status
from rest_framework.response import Response


class DealsView(viewsets.ViewSet):
    """
    URL: /deals/
    METHODS: GET, POST

    Реаализует создание записей в БД и получение данных о топ пяти клиентах
    """
    cash = None

    def list(self, request):
        """
        METHOD: GET

        Проверяет кэш, если он есть отдаёт его, если пусто:
        находит топ пять клиентов и сумму их трат, потом в цикле находит для каждого список камней.
        Надо уйти от запросов в цикле и получать все необходимые данные
        одним запросом.

        return: лист словарей или пустой лист
        """
        if DealsView.cash:
            return Response(DealsView.cash)

        else:

            customer_qs = Customer.objects.filter(deal__isnull=False)
            customer_qs = customer_qs.annotate(amount__sum=Sum('deal__amount')).order_by('-amount__sum')[:5]
            customer_ids = [i.id for i in customer_qs]
            data = []

            for index, customer in enumerate(customer_qs):
                another_best = customer_ids[:index] + customer_ids[index+1:]
                gem_qs = Gem.objects.filter(deal__customer__id__in=another_best).distinct('id')
                gem_qs = gem_qs.filter(deal__customer__id=customer.id).all()
                data.append({
                    'username': customer.name,
                    'spent_money': customer.amount__sum,
                    'gems': [i.name.capitalize() for i in gem_qs]
                })

            DealsView.cash = data

            return Response(data)

    def create(self, request):
        """
        METHOD: POST

        Очищает кэш, инициализиурет парсер, передаёт в него CSV. Если всё ок, создаёт двумя транзакциями
        несуществующих клиентов и камни. На их основне создает сделки и добавляет их одной транзакцией.

        return: 200 {'message': 'success'} или 400 {"error": <описание_ошибки_валидации>}

        Можно было обойтись серелизаторами и не городить всё это. Но в случае использования серелизаторов
        среднее время создания 800 элементов составляло 3 секунды, данный подход позволил сократить его
        до 0.25. Использовать серелизаторы и просто навесить transaction.atomic на функцию не получилось,
        потому что для создания Deal нужны pk Gem и Customer """

        DealsView.cash = None

        pars = Parser()
        data = request.data['deals']
        try:
            customers, gems, deals = pars.parse(data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        customers_dict = create_inexistent_items(customers, Customer)
        gems_dict = create_inexistent_items(gems, Gem)

        deals_obj = [
            Deal(
                amount=i['amount'],
                quantity=i['quantity'],
                date=i['date'],
                customer=customers_dict[i['customer']],
                gem=gems_dict[i['gem']]
            )
            for i in deals
        ]

        Deal.objects.bulk_create(deals_obj)

        return Response({'message': 'success'})

