from django_unicorn.components import UnicornView
from django.db.models import Q
from investors.models import Investor

class FilterView(UnicornView):
    
    filters_list = (
        ['zip_code', "Zip code"],
        ['country_to_invest', "Countries to Invest"],
        ['city', 'Cities'],
        ['state', 'States']
    )
    filter_by = ''
    filter_value = ""
    investors = None

    def mount(self, *args, **kwargs):
        self.filter()

    def filter(self, *args):
        if not self.filter_by:
            self.filter_by = 'all'
        print(self.filter_by, ',' ,self.filter_value)
        self.investors = Investor.objects.all()
        if self.filter_by and self.filter_value:
            if self.filter_by == 'all':
                query = None
                for filter_type in self.filters_list:
                    if query:
                        query = query | Q(**{f'{filter_type[0]}__icontains': self.filter_value})
                    else:
                        query = Q(**{f'{filter_type[0]}__icontains': self.filter_value})

                self.investors = self.investors.filter(query)
                return
            else:
                query = {f'{self.filter_by}__icontains': self.filter_value}
                self.investors = self.investors.filter(**query)
                return
        print('filter did not work')
    
    def updated_filter_by(self, *args):
        self.filter()

    def updated_filter_value(self, *args):
        self.filter()