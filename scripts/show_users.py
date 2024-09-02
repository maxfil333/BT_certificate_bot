from src.sql_queries import execute


if __name__ == '__main__':
    print(execute('select * from users'), sep='\n')