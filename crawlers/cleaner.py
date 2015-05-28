from os import listdir
from os.path import isfile, join
import sqlite3


def write_to_file(content, new_file_name):
    new_file = open(new_file_name, 'w')
    new_file.write(content)
    new_file.close()



STOP_CONDITION = 16556

# Create database and get cursor
db = sqlite3.connect('news.db')
c = db.cursor()

# Create table if not exists
tb_exists = "SELECT name FROM sqlite_master WHERE type='table' AND name='news'"
if not c.execute(tb_exists).fetchone():
   c.execute("CREATE TABLE news (url text primary key, title text, text_file text)")

# Gather files
files = [ f for f in listdir("dump") if isfile(join("dump", f)) ]
fileNr = 0

for file in files:
    news = open("dump/" + file, 'r')
    lineNr = 0
    fullLineCount = 0;
    url = ""; title = "";
    content = ""


    # Read lines data
    for line in news.readlines():
        if lineNr==0:
            url = line
        elif lineNr==1:
            title = line
        elif not line=="\n":
            # Clean here
            if len(line)<40:
                line = line.rstrip()
            content += line.lstrip()
            fullLineCount += 1

        lineNr += 1


    if len(content)<150:
        continue;
    if fullLineCount<3:
        continue;

    # Save in database
    args = (url.decode("utf-8"), title.decode("utf-8"), file.decode("utf-8"), )

    try:
        c.execute("INSERT INTO news VALUES (?,?,?)", args)

        # Stop condition
        fileNr += 1
        if fileNr==STOP_CONDITION:
            break;


        write_to_file(content, "readynews/" + file)
    except sqlite3.IntegrityError:
        # It means there is this url!
        # Duplicate!
        print "Duplicate: " + file


db.commit();
