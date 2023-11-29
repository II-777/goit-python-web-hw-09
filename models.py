from mongoengine import Document, StringField, DateTimeField, ReferenceField, ListField

class Authors(Document):
    fullname = StringField(required=True)
    born_date = DateTimeField()
    born_location = StringField()
    description = StringField()
    meta = {'db_alias': 'default'}

class Quotes(Document):
    tags = ListField(StringField())
    author = ReferenceField(Authors, reverse_delete_rule=2)
    quote = StringField()
    meta = {'db_alias': 'default'}

if __name__ == "__main__":
    pass

