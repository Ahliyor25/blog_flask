from peewee import *  

def get_db():
    database = SqliteDatabase('Blog.db')
    database.connect()
    return database


database = get_db()


class BaseModel(Model):
    class Meta:
        database = database

class Users(BaseModel):
	id = IntegerField(primary_key=True)
	username = CharField()
	password = CharField()
	name = CharField()
	email = CharField()
	phone = CharField(default = "")


class BlogPost(BaseModel):
    id = IntegerField(primary_key=True)
    title = CharField()
    text = TextField()
    published = DateField()
    ownerusername = ForeignKeyField(Users, related_name='UserId')
    likes = IntegerField(default = 0)
    dislikes = IntegerField(default = 0)
    

class Comments(BaseModel):
    id = IntegerField(primary_key = True)
    text = TextField()
    postid = ForeignKeyField(BlogPost, related_name='BlogPost')
    ownerusername = ForeignKeyField(Users, related_name = 'Users')
    likes = IntegerField(default = 0)
    dislikes = IntegerField(default = 0)





if __name__ == '__main__':
    Users.create_table()
    BlogPost.create_table()
    Comments.create_table()
