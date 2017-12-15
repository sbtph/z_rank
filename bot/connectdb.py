import psycopg2
import platform

def connectdb():
    info = platform.platform()
    if 'Windows' in info:
        return psycopg2.connect(database="zrank", user="postgres", \
                         password="syiloveu559", host="localhost", port="5432")
    else:
        return psycopg2.connect(database="zrank", user="ban11111", \
                         password="syiloveu559")