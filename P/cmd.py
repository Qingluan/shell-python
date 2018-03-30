import os
from argparse import ArgumentParser
from .lang import LangTree

Arger = ArgumentParser()
# Arger.add_argument("-s", "--session", default=False, action='store_true', help="update proxy...")
Arger.add_argument("shell", nargs="*", help="run")
Arger.add_argument("-s", "--switch", default=None, help="set a session")



def run():
    args = Arger.parse_args()
    if args.switch:
        with open("/tmp/session", "w") as fp:
            fp.write(args.switch)
    

    
    if os.path.exists("/tmp/session"):
        token = "test"
        with open("/tmp/session") as fp:
            token = fp.readline().strip()
            l = LangTree.Tree(token)

            w = ' '.join(args.shell)
            l.cal("%list")
            l.cal(w)
            l.sess.save()

