# -*- coding: utf-8 -*-

import sqlite3


class DBHelper:
    
    def __init__(self, dbname="main.sqlite"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname, check_same_thread=False)
        self.c = self.conn.cursor()

    def setup(self):
        stmt = """CREATE TABLE IF NOT EXISTS data (tlgrm_id INTEGRER NOT NULL,
                                                   insta_user DEFAULT none,                                                  
                                                   warnings DEFAULT 0,
                                                   admin DEFAULT none)"""
        self.c.execute(stmt)
        self.conn.commit()

    def add_tlgrm_user(self, tlgrm_id, insta_user):
        self.c.execute("INSERT INTO data (tlgrm_id, insta_user) VALUES (?, ?)", (tlgrm_id, insta_user))
        self.conn.commit()

    def add_insta_user(self, insta_user):
        self.c.execute("INSERT INTO data (insta_user) VALUES (?)", (insta_user, ))
        self.conn.commit()

    def add_admin(self, tlgrm_id):
        admin = True
        self.c.execute("UPDATE data SET admin=? WHERE tlgrm_id=?", (admin, tlgrm_id))
        self.conn.commit()

    def del_admin(self, tlgrm_id):
        admin = False
        self.c.execute("UPDATE data SET admin=? WHERE tlgrm_id=?", (admin, tlgrm_id))
        self.conn.commit()

    def get_admin(self, tlgrm_id):
        self.c.execute("SELECT admin FROM data WHERE tlgrm_id=?", (tlgrm_id, ))
        admin = self.c.fetchone()
        return admin[0]

    def get_tlgrm_user(self, tlgrm_id):
        self.c.execute("SELECT tlgrm_id FROM data WHERE tlgrm_id=?", (tlgrm_id, ))
        user = self.c.fetchone()
        if user is not None:
            return user[0]
        else:
            return None

    def get_tlgrm_id(self, insta_user):
        self.c.execute("SELECT tlgrm_id FROM data WHERE insta_user=?", (insta_user, ))
        user = self.c.fetchone()
        if user is not None:
            return user[0]
        else:
            return None

    def del_tlgrm_user(self, tlgrm_id):
        self.c.execute("DELETE FROM data WHERE tlgrm_id=?", (tlgrm_id, ))
        self.conn.commit()

    def get_insta_username(self, insta_username):
        self.c.execute("SELECT insta_user FROM data WHERE insta_user=?", (insta_username, ))
        insta_user = self.c.fetchone()
        if insta_user is not None:
            return str(insta_user[0])
        else:
            return None

    def get_insta_user(self, tlgrm_id):
        self.c.execute("SELECT insta_user FROM data WHERE tlgrm_id=?", (tlgrm_id, ))
        insta_user = self.c.fetchone()
        if insta_user is not None:
            return str(insta_user[0])
        else:
            return None

    def change_insta_user(self, insta_user, tlgrm_id):
        self.c.execute("UPDATE data SET insta_user=? WHERE tlgrm_id=? ", (insta_user, tlgrm_id))
        self.conn.commit()

    def add_warning(self, insta_user):
        warnings = self.get_warnings(insta_user)
        warnings += 1
        self.c.execute("UPDATE data SET warnings=? WHERE insta_user=?", (warnings, insta_user))
        self.conn.commit()

    def get_warnings(self, insta_user):
        self.c.execute("SELECT warnings FROM data WHERE insta_user=?", (insta_user, ))
        points = self.c.fetchone()
        return int(points[0])

    def refresh(self):
        points = 0
        warnings = 0
        self.c.execute("UPDATE data SET points=?, warnings=?", (points, warnings))
        self.conn.commit()

    def del_warning(self, insta_username):
        warnings = self.c.execute("SELECT warnings FROM data WHERE insta_user=?", (insta_username, ))
        warnings = self.c.fetchone()
        warnings = int(warnings[0])
        print warnings
        self.c.execute("UPDATE data SET warnings=? WHERE insta_user=?", ((warnings - 1), insta_username))
        self.conn.commit()

    def all_warnings(self):
        self.c.execute("SELECT insta_user, warnings FROM data")
        warnings = self.c.fetchall()
        return warnings

    def all_admins(self):
        self.c.execute("SELECT insta_user FROM data WHERE admin=1")
        admins = self.c.fetchall()
        return admins


