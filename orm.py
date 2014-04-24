__author__ = 'vinogradov'


class Filter(object):
    def __init__(self, param1, param2):
        self.param1 = param1
        self.param2 = param2
        super(Filter, self).__init__()


class CMPFilter(Filter):
    def to_sql(self):
        return repr(self.param1) + '=' + repr(self.param2)


class Field(object):

    def __init__(self, tablename, fieldname):
        self.tablename = tablename
        self.fieldname = fieldname
        super(Field, self).__init__()

    def __eq__(self, other):
        return CMPFilter(self, other).to_sql()

    def __repr__(self):
        return self.tablename + '.' + self.fieldname


class Table(object):

    def __init__(self, tablename):
        self.tablename = tablename
        super(Table, self).__init__()

    def __getattr__(self, item):
        try:
            return self.__getattribute__(item)
        except AttributeError:
            return Field(tablename=self.tablename, fieldname=item)


class ModelParser(object):
    select_section = str
    filter_section = str

    def filter(self, *args):
        self.filter_section = None

        for item in args:
            if self.filter_section is None:
                self.filter_section = 'WHERE ' + item
            else:
                self.filter_section += ' AND ' + item

        print(self.filter_section)

        print('TOTAL:')
        print(self.select_section + ' ' + self.filter_section)
        return self

    def select(self, *args):
        self.select_section = None
        tablelist = set()
        for item in args:
            table = item.tablename
            field = item.fieldname
            tablelist.update([table])
            i = table + '.' + field
            if self.select_section is None:
                self.select_section = 'SELECT ' + str(i)
            else:
                self.select_section += ', ' + str(i)

        self.select_section += ' FROM ' + ', '.join(tablelist)

        print(self.select_section)
        return self

mymodel = ModelParser()
t1 = Table('user')
t2 = Table('city')
mymodel.select(t1.name, t2.newname).filter(t1.id==1, t2.myid==t1.city_id)