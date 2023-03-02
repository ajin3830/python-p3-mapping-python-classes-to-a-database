from config import CONN, CURSOR

class Song:
    # __init__ method creates a new instance of the song class
    # , a new Python object.
    def __init__(self, name, album):
        # initializing an individual Song instance with 
        # an id attribute that has a default value of None
        # id attribute value is None when a new song is created
        # only when a song is saved into the database 
        # SQL gives a unique id value which is the PRIMARY KEY
        # for each table row
        # INTEGER PRIMARY KEY datatype will assign and auto-increment 
        # the id attribute of each record that gets saved
        self.id = None
        self.name = name
        self.album = album

    @classmethod
    # to map Song class to a database table, 
    # pluralize the name of the class to create the name of the table
    def create_table(cls):
        # SQL statement to create a songs table 
        # and give that table column names that match 
        # the attributes of an individual instance of Song
        sql = """
            CREATE TABLE IF NOT EXISTS songs (
            id INTEGER PRIMARY KEY,
            name TEXT,
            album TEXT
            )
        """

        CURSOR.execute(sql)

# NOW run these commands
# python lib/debug.py
# Song.create_table() doesn't return anything bc no data in table yet
# CURSOR.execute("PRAGMA table_info(songs)").fetchall() shows info about table

    # insert data into a table with instance method save()
    # to save a song into the songs table, use the name and album 
    # of the song to create a new row in that table
    # save() is not saving the Python object itself.
    # It's creating a new row in songs table that has the attributes 
    # that characterize that song instance.
    def save(self):
        # to pass in name and album into Python string
        # use ? characters as placeholders
        sql = """
            INSERT INTO songs (name, album)
            VALUES (?, ?)
        """
        # Cursor.execute() method takes the values passed in as an argument
        # and apply them as the values of the question marks.
        CURSOR.execute(sql, (self.name, self.album))
        CONN.commit()

    # BC we might not want to save an object everytime we create one
    # we'll keep our __init__ and save() methods separate as above

# now run these commands
# python lib/debug.py
# hello=Song('Hello', '25')
# hello.save() returns an empty array once more since 
# INSERTing new rows in a database doesn't return any data
# so run this to check if all records were saved
# songs = CURSOR.execute('SELECT * FROM songs')
# [row for row in songs]

    # Grab the id of that newly inserted row 
    # and assigning the given Song instance's id attribute 
    # equal to the id of its associated database table row.
        self.id = CURSOR.execute("SELECT last_insert_rowid() FROM songs").fetchone()[0]

# now run these commands
# python lib/debug.py
# hello = Song("Hello", "25")
# hello.save()
# hello.id returns 1

# HOWEVER
# Any time we see the same code being used again and again, 
# we think about abstracting that code into a method.
    @classmethod
    # use keyword arguments to pass a name and album
    def create(cls, name, album):
        # use that name and album to instantiate a new song
        song = Song(name, album)
        # use the save method to persist that song to the database
        song.save()
        # The return value should always be the object that you created
        # so you don't have to run a separate query on our database
        # to grab the record that you just created
        return song
