#!/bin/python

import unittest
import os
from bitfeeds.storage.file import FileStorage
from bitfeeds.util import Logger

path = 'tests/'
table_name = 'test_query'
columns = ['date', 'time', 'k', 'v', 'v2']
types = ['text', 'text', 'int PRIMARY KEY', 'text', 'decimal(10,5)']

class SqliteClientTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        Logger.init_log()
        cls.storage = FileStorage(dir=path)
        cls.storage.connect()

    @classmethod
    def tearDownClass(cls):
        cls.storage.close()
        os.remove(path + table_name + ".csv")

    def test_query(self):
        # Check table creation
        self.assertTrue(self.storage.create(table_name, columns, types))

        # Check table insertion
        self.assertTrue(
            self.storage.insert(table=table_name, columns=columns, types=types,
            values=['20161026','10:00:00.000000',1,'AbC',10.3]))
        
        # insert(self, table, columns, types, values, primary_key_index=[], is_orreplace=False, is_commit=True)
        
        self.assertTrue(self.storage.insert(
            table_name,
            columns,
            types,
            ['20161026','10:00:01.000000',2,'AbCD',10.4]))
        
        self.assertTrue(self.storage.insert(
            table_name,
            columns,
            types,
            ['20161026','10:00:02.000000',3,'Efgh',10.5]))

        # # Fetch the whole table
        row = self.storage.select(table=table_name)
        self.assertEqual(len(row), 3)
        self.assertEqual(row[0][0], "20161026")
        self.assertEqual(row[0][1], "10:00:00.000000")
        self.assertEqual(row[0][2], 1)
        self.assertEqual(row[0][3], 'AbC')
        self.assertEqual(row[0][4], 10.3)
        self.assertEqual(row[1][0], "20161026")
        self.assertEqual(row[1][1], "10:00:01.000000")
        self.assertEqual(row[1][2], 2)
        self.assertEqual(row[1][4], 10.4)
        self.assertEqual(row[1][3], 'AbCD')
        self.assertEqual(row[2][0], "20161026")
        self.assertEqual(row[2][1], "10:00:02.000000")
        self.assertEqual(row[2][2], 3)
        self.assertEqual(row[2][3], 'Efgh')
        self.assertEqual(row[2][4], 10.5)

        # Fetch with condition
        row = self.storage.select(table=table_name, condition="k=2")
        self.assertEqual(len(row), 1)
        self.assertEqual(row[0][0], "20161026")
        self.assertEqual(row[0][1], "10:00:01.000000")
        self.assertEqual(row[0][2], 2)
        self.assertEqual(row[0][3], 'AbCD')
        self.assertEqual(row[0][4], 10.4)

        # # Fetch with ordering
        row = self.storage.select(table=table_name, orderby="k desc")
        self.assertEqual(len(row), 3)
        self.assertEqual(row[2][0], "20161026")
        self.assertEqual(row[2][1], "10:00:00.000000")
        self.assertEqual(row[2][2], 1)
        self.assertEqual(row[2][3], 'AbC')
        self.assertEqual(row[2][4], 10.3)
        self.assertEqual(row[1][0], "20161026")
        self.assertEqual(row[1][1], "10:00:01.000000")
        self.assertEqual(row[1][2], 2)
        self.assertEqual(row[1][3], 'AbCD')
        self.assertEqual(row[1][4], 10.4)
        self.assertEqual(row[0][0], "20161026")
        self.assertEqual(row[0][1], "10:00:02.000000")
        self.assertEqual(row[0][2], 3)
        self.assertEqual(row[0][3], 'Efgh')
        self.assertEqual(row[0][4], 10.5)

        # Fetch with limit
        row = self.storage.select(table=table_name, limit=1)
        self.assertEqual(len(row), 1)
        self.assertEqual(row[0][0], "20161026")
        self.assertEqual(row[0][1], "10:00:00.000000")
        self.assertEqual(row[0][2], 1)
        self.assertEqual(row[0][3], 'AbC')
        self.assertEqual(row[0][4], 10.3)

        # Select with columns
        row = self.storage.select(table=table_name, columns=['k', 'v'])
        self.assertEqual(len(row), 3)
        self.assertEqual(row[0][0], 1)
        self.assertEqual(row[0][1], 'AbC')
        self.assertEqual(row[1][0], 2)
        self.assertEqual(row[1][1], 'AbCD')
        self.assertEqual(row[2][0], 3)
        self.assertEqual(row[2][1], 'Efgh')

        # # Negative case
        self.assertTrue(not self.storage.create(table_name, columns[1::], types))
        self.assertTrue(not self.storage.insert(table_name, columns, types, []))

if __name__ == '__main__':
    unittest.main()

