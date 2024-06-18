import sqlite3
from . import Connection

def getMlfbByHwType(hw_type):
    cursor = Connection.getCursor()
    cursor.execute('SELECT mlfb FROM CPU_List WHERE type = ?', (hw_type,))
    return cursor.fetchall()

def getMlfbIHMByHwType(hw_type):
    cursor = Connection.getCursor()
    cursor.execute('SELECT mlfb FROM IHM_List WHERE type = ?', (hw_type,))
    return cursor.fetchall()

def getMlfbIHMByVersion(hw_type):
    cursor = Connection.getCursor()
    # Realiza a união das tabelas IHM_List e CPU_List com a tabela VersoesHardware para obter as versões correspondentes
    query = """
    SELECT VersoesHardware.mlfb, VersoesHardware.versao
    FROM IHM_List
    JOIN VersoesHardware ON IHM_List.mlfb = VersoesHardware.mlfb
    WHERE IHM_List.type = ?
    UNION
    SELECT VersoesHardware.mlfb, VersoesHardware.versao
    FROM CPU_List
    JOIN VersoesHardware ON CPU_List.mlfb = VersoesHardware.mlfb
    WHERE CPU_List.type = ?
    """
    # Passa o mesmo tipo de hardware para ambas as partes da união
    cursor.execute(query, (hw_type, hw_type))
    return cursor.fetchall()