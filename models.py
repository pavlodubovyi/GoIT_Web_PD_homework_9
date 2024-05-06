from mongoengine import connect, Document, StringField, ReferenceField, ListField, CASCADE, BooleanField

connect(db="PD_homework_8", host="mongodb+srv://userweb21:567234@cluster0.vkwfwwg.mongodb.net/")


class Author(Document):
    fullname = StringField(required=True, unique=True)
    born_date = StringField(max_length=50)
    born_location = StringField(max_length=150)
    description = StringField()
    meta = {"collection": "authors"}


class Quote(Document):
    author = ReferenceField(Author, reverse_delete_rule=CASCADE)
    tags = ListField(StringField())
    quote = StringField()
    meta = {"collection": "quotes"}
