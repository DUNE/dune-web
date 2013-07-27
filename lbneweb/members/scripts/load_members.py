from members.loader import Data
from members.loader import make_role_table, purge_db


def run(argv):
    if 'purge' in argv:
        purge_db()
    if 'roles' in argv:
        make_role_table()
    if 'members' in argv:
        x = Data()
        x.load()
