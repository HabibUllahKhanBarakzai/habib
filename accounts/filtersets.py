# import django_filter
# from django.db.models import Count, Q, Value
# from django.db.models.functions import Concat
# from django.db.models import Q
#
# from accounts.models import Mobile
#
#
# class MobileFilter(django_filter.FilterSet):
#     class Meta:
#         model = Mobile
#         fields = {
#             "IMEA_number": ['exact', 'in', 'icontains'],
#             "type": ['exact', 'in', 'icontains']
#         }