import sqlite3


def createCandleTable(exchangeName, pair, duration):

    setTableName = str(exchangeName + "_" + pair + "_" + duration)
    conn = sqlite3.connect('candleDatabase.db')
    cur = conn.cursor()

    tableCreationStatement = """CREATE TABLE """ + setTableName + """(Id INTEGER PRIMARY KEY, date INT, high REAL, low REAL, open REAL, close REAL, volume REAL, quotevolume REAL, sma_7 REAL, ema_7 REAL, sma_30 REAL, ema_30 REAL, sma_200 REAL, ema_200 REAL)"""
    cur.execute(tableCreationStatement)

    conn.commit()
    conn.close()


def createFullDatasetTable(exchangeName, pair):

    setTableName = str(exchangeName + "_" + pair)

    #return (setTableName)
    conn = sqlite3.connect('candleDatabase.db')
    cur = conn.cursor()

    tableCreationStatement = """CREATE TABLE """ + setTableName + """(Id INTEGER PRIMARY KEY, uuid TEXT, traded_btc REAL, price REAL, created_at_int INT, side TEXT)"""
    cur.execute(tableCreationStatement)

    conn.commit()
    conn.close()


def createTrackOfUpdateTable():

    conn = sqlite3.connect('candleDatabase.db')
    cur = conn.cursor()

    tableCreationStatement = """ CREATE TABLE last_checks(Id INTEGER PRIMARY KEY, exchange TEXT, trading_pair TEXT, duration TEXT, table_name TEXT, last_check INT, startdate INT, last_id INT) """
    cur.execute(tableCreationStatement)

    conn.commit()
    conn.close()


createCandleTable('Binance', 'ETHBUSD', '5m')
createFullDatasetTable('Binance', 'ETHBUSD')
createTrackOfUpdateTable()
