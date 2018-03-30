import re
import importlib
from termcolor import colored, cprint
from ._libs import Sess

class PyError(Exception):
    pass


class LangTree:
    def __init__(self, sess):
        self.sess = sess

    def module(self, string):
        group = re.match(r'^(?P<l>import|from)\s+(?P<lc>(?:\w+\.?)+)\s*(?P<r>import)?\s*(?P<rc>(?:\w+\.?)*)\s*(as)?\s*(?P<n>\w+)?', string)
        if not group:
            return
        if not group.group("l"):
            return

        import_str = group.group("lc")
        attrs = None

        if group.group("l") == 'from':
            if group.group("r") != 'import' or not group.group("rc"):
                return
            attrs = group.group("rc")
        
        
        name = group.group("n")
        lib = importlib.import_module(import_str)

        if attrs:
            lib = getattr(lib, attrs)

        if not name:
            name = lib.__name__
        
        self.sess.add_attr(name, lib)
        return True

    def cmd(self, string):
        if string[1:] == "list":
            for i in self.sess._attres.__dict__:
                cprint(i + " =>" + str(self.sess._attres.__dict__[i]), 'green')

    def cal(self, string):
        # if "==" in string:
            # pass
        # elif "=" in string:
            # name, string = string.split("=")
        if string.startswith("%"):
            self.cmd(string)
            return

        if self.module(string):
            return

        words = string.split()
        values = []
        # print(words)
        # vv = None
        for i in words:
            c_words = re.findall(r'\w+', i)
            vv = i
            # print(c_words)
            for c in c_words:
                gg = self.sess.search(c)
                vv = vv.replace(c, gg)
                

            values.append(vv)

        vl = " ".join(values)
        name = ["_"]
        names_i = -1
        if '=' in vl:
            names_i = vl.index("=")

            name = vl[:names_i].split(",")
            if not name:
                name = ["_"]
        try:
            res = eval(vl[names_i+1:])
            if len(name) > 1:
                for i,r in enumerate(res):
                    self.sess.add_attr(name[i], r)
            elif len(name) == 1:
                self.sess.add_attr(name[0], res)
                if name[0] == "_":
                    print(res)
            else:
                raise PyError(string + " => " + ' '.join(vl))
        except NameError:
            
            raise PyError(' '.join(values))

    @classmethod
    def Tree(cls, label="py"):
        s = Sess(label)
        return cls(s)