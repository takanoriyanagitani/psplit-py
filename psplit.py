import os
import sys
import functools
import operator
from itertools import groupby

def psplit_key2name(key=0, basedir=".", ext=".txt"):
  return os.path.join(basedir, str(key) + ext)

def psplit_sfunc(t=tuple(), hwm=4):
  i = t[0]
  j = i >> hwm
  return j

def psplit_str2file(s, name, tname=""):
  tname = tname or operator.add(name, ".temp")
  bdir = os.path.dirname(tname)
  os.makedirs(bdir, exist_ok=True)
  with open(tname, "w") as f:
    f.write(s)
    f.flush()
    os.fdatasync(f.fileno())
  os.rename(tname, name)
  return 1

def psplit_write(
  t=tuple(),
  bdir=".",
  key2name=psplit_key2name,
  prefix="",
  suffix="",
  separator="\n",
  str2file=psplit_str2file,
  tuple2line=operator.itemgetter(1),
):
  k = t[0]
  g = t[1]
  n = key2name(k, bdir)
  lines = map(tuple2line, g)
  joined = separator.join(lines)
  return str2file(prefix + joined + suffix, n)

def psplit(
  i=iter([]),
  bdir=".",
  sfunc=psplit_sfunc,
  key2name=psplit_key2name,
  line2tuple=enumerate,
  prefix="",
  suffix="",
  separator="\n",
  str2file=psplit_str2file,
  tuple2line=operator.itemgetter(1),
  prefilter=operator.methodcaller("strip"),
):
  t = line2tuple(map(prefilter, i))
  g = groupby(t, sfunc)
  p = functools.partial(
    psplit_write,
    bdir=bdir,
    key2name=key2name,
    prefix=prefix,
    suffix=suffix,
    separator=separator,
    str2file=str2file,
  )
  writes = map(p, g)
  wrote_count = sum(writes)
  return wrote_count

def main(): return psplit(sys.stdin, "splited", prefix="[", suffix="]", separator=",")

def try_exec(): return "__main__" == __name__ and print("wrote count: " + str(main()))

try_exec()
