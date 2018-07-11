# SQL Database
import sqlite3

# Establish Connection With The Server
cnct = sqlite3.connect('example_table.db')
print ("Database Opened Successfully")

# Create The Table
cnct.execute('''CREATE TABLE Company
         (ID            INT PRIMARY KEY     NOT NULL,
         NAME           TEXT                NOT NULL,
         ADDRESS        CHAR(50)                    ,
         FOUNDED        DATE                        );''')
print ("Table created Successfully");

# Add Values Into The Table
cnct.execute("INSERT INTO Company (ID, NAME, ADDRESS, FOUNDED) \
              VALUES (1, 'google', '1600, Amphitheatre Parkway, Mountain View, California, United States', '1998/9/4')");
cnct.execute("INSERT INTO Company (ID, NAME, ADDRESS, FOUNDED) \
              VALUES (2, 'nintendo', 'Kyoto, Japan, 11-1 Kamitoba-hokotate-cho, Minami-ku, Kyoto 601-8501', '1889/9/23')");
cnct.execute("INSERT INTO Company (ID, NAME, ADDRESS, FOUNDED) \
              VALUES (3, 'microsoft', 'Microsoft Headquarters One Microsoft Way Redmond, WA 98052', '1975/4/4')");

# Save Changes
cnct.commit()
cnct.close()
