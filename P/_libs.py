import sys,os

import dill as pickle
from contextlib import contextmanager

import termcolor

ROOT = "/tmp/psession"

if not os.path.exists(ROOT):
    os.mkdir(ROOT)

@contextmanager
def stdout(f):
    try:
        tmp = sys.stdout
        sys.stdout = f
        yield
    except Exception as e:
        raise e
    finally:
        sys.stdout = tmp


class _attrs:
    pass

class _functions:
    pass

class Sess:

    def __init__(self, token):
        self.token = token
        self.tmp_file = os.path.join(ROOT,token)
        self._attres = _attrs()
        if not os.path.exists(self.tmp_file):
            self.save()
        self.load()
        # self._functions = _functions()

    def save(self):
        # with open(self.tmp_file+"f", "wb") as fp:
            # pickle.dump(self._functions,fp)

        with open(self.tmp_file, "wb") as fp:
            pickle.dump(self._attres,fp)

    def load(self):
        if not os.path.exists(self.tmp_file):
            termcolor.cprint("no such file", "red")
            return 

        # with open(self.tmp_file + "f", "rb") as fp:
        #     self._functions = pickle.load(fp)

        with open(self.tmp_file, "rb") as fp:
            self._attres = pickle.load(fp)

    def __getitem__(self,k):
        return self._attres.__dict__.get(k, None)

    def search(self,w):
        if hasattr(self._attres, w):
            return "self.sess._attres." + w
        return w

    def add_attr(self,w,v):
        if not "self.sess._attres." in w:
            setattr(self._attres, w.strip(), v)
        else:
            w = w.replace("self.sess._attres.", "")
            
            setattr(self._attres, w.strip(), v)
            

