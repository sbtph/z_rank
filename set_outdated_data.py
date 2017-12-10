# coding: utf-8
import datetime
import psycopg2
import psycopg2.extras

class set_outdated_data(object):

    def __init__(self, day):
        self.now = datetime.datetime.now()
        self.day = day
        self.datestring  = ''
        try:
            self.conn = psycopg2.connect(database="smzdm", user="postgres", \
            password="syiloveu559", host="localhost", port="5432")
            self.cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        except Exception as e:
            print ('Connect to db failed!')
            print (e)

    def process(self):
        self.cur.execute("select posted_at from zrank;")
        date_list = [j for i in self.cur.fetchall() for j in i]
        print (date_list)
        for date in date_list:
            self.datestring = datetime.datetime.strftime(date,'%Y-%m-%d %H:%M')
            print (self.datestring)
            if (self.now - date).days > self.day - 1:
                self.cur.execute("update zrank set outdated = TRUE where posted_at = %s",str(self.datestring))
                self.conn.commit()
            else:
                self.cur.execute("update zrank set outdated = FALSE where posted_at = %s",[self.datestring,])
                self.conn.commit()
        self.cur.close()
        self.conn.close()

#set_outdated_data(1).process()
