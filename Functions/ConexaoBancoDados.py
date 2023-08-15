import pyodbc 

def conexao_banco_Dados():
    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                        'Server=SAFBRDB01;'
                        'Database=MIDDLESAFIRA;'
                        'Trusted_Connection=yes')
                        # "uid=usrmiddlesafira;pwd=0LOPoA@mLZRPpB")



    return conn



