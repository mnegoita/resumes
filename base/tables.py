import django_tables2 as tables
from .models import Category, Tag




class BaseTable(tables.Table):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Text to return if empty
        if self.empty_text is None:
            self.empty_text = 'No {} found yet'.format(self._meta.model._meta.verbose_name_plural)

    class Meta:
        attrs = {
            'class': 'table table-sm'
        }


class CategoryTable(BaseTable):
    name = tables.LinkColumn()

    class Meta(BaseTable.Meta):
        model = Category
        fields = ('name', )


class TagTable(BaseTable):
    name = tables.LinkColumn()

    class Meta(BaseTable.Meta):
        model = Tag
        fields = ('name', )
        


