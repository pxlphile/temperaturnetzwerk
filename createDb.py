#!/usr/bin/env python
import sqlite3

# Creates the initial database structure in the current directory.
#
# Please note: The table column names correspond directy to those in
# thermo.py. If you plan to change the column names please change them
# in both files.

# please refer to the sqlite documentation for naming conventions
databaseFilePath = "./temperatur.db"
databaseTableName = "temperatur"
databaseColumnDate = "tempDate"
databaseColumnTemperature = "temperature"
databaseColumnSensorId = "sensorId"

def main():
    conn = sqlite3.connect(databaseFilePath)
    c = conn.cursor()
    print "Create sqlite database" + databaseFilePath

    c.execute("""
CREATE TABLE `""" + databaseTableName + """` (\
`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, \
`""" + databaseColumnDate + """`		text, \
`""" + databaseColumnTemperature + """`	real, \
`""" + databaseColumnSensorId + """`	text);""")
    conn.commit()

    c.execute("""CREATE INDEX colDateIdx ON """ + databaseTableName + """(""" + databaseColumnDate + """)""")
    conn.commit()

    c.execute("""CREATE INDEX sensorIdx ON """ + databaseTableName + """(""" + databaseColumnSensorId + """)""")
    conn.commit()

    conn.close()

if __name__ == '__main__':
    main()
