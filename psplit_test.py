import os
import functools

import psplit

def test_psplit_key2name():
  assert os.path.join(".", "0.txt") == psplit.psplit_key2name()
  assert os.path.join(".", "1.txt") == psplit.psplit_key2name(1)
  assert os.path.join("a", "1.txt") == psplit.psplit_key2name(1, "a")
  assert os.path.join("a", "1.csv") == psplit.psplit_key2name(1, "a", ".csv")

def test_psplit_sfunc():
  assert 0 == psplit.psplit_sfunc((0, None))
  assert 0 == psplit.psplit_sfunc((1, None))
  assert 0 == psplit.psplit_sfunc((2, None))
  assert 0 == psplit.psplit_sfunc((4, None))
  assert 0 == psplit.psplit_sfunc((8, None))
  assert 0 == psplit.psplit_sfunc((15, None))
  assert 1 == psplit.psplit_sfunc((16, None))
  assert 0 == psplit.psplit_sfunc((16, None), hwm=8)
  assert 0 == psplit.psplit_sfunc((255, None), hwm=8)
  assert 1 == psplit.psplit_sfunc((256, None), hwm=8)

def test_psplit_str2file():
  tdir = "test_dir"
  os.makedirs(tdir, exist_ok=True)
  j = lambda n: os.path.join(tdir, n)

  psplit.psplit_str2file("hw", j("t1.txt"))
  with open(j("t1.txt")) as f: assert(f.read() == "hw")

  psplit.psplit_str2file("[1,2,3]", j("t2.json"))
  with open(j("t2.json")) as f: assert(f.read() == "[1,2,3]")
  pass

def test_psplit_write():
  i = range(3)
  s = map(str, i)
  l = list(enumerate(s))
  t = (0, l)
  bdir = "test_dir"

  assert 1 == psplit.psplit_write(t, bdir)
  with open(os.path.join(bdir, "0.txt")) as f: assert "0\n1\n2" == f.read()

  key2name = functools.partial(psplit.psplit_key2name, ext=".csv")
  assert 1 == psplit.psplit_write(t, bdir, key2name)
  with open(os.path.join(bdir, "0.csv")) as f: assert "0\n1\n2" == f.read()

  key2name = functools.partial(psplit.psplit_key2name, ext=".json")
  prefix   = "["
  suffix   = "]"
  separator = ","
  assert 1 == psplit.psplit_write(t, bdir, key2name, prefix, suffix, separator)
  with open(os.path.join(bdir, "0.json")) as f: assert "[0,1,2]" == f.read()

  def str2file(s, name, tname=""):
    with open(name, "w") as f: return f.write(s)
  assert 5 == psplit.psplit_write(t, bdir, str2file=str2file)
  with open(os.path.join(bdir, "0.txt")) as f: assert "0\n1\n2" == f.read()

  tuple2line = lambda t: t[2]
  assert 1 == psplit.psplit_write((0, [(0, "line", "3rd")]), bdir, tuple2line=tuple2line)
  with open(os.path.join(bdir, "0.txt")) as f: assert "3rd" == f.read()

  pass

def test_psplit():
  assert  1 == psplit.psplit(map(str, range(   1)))
  assert  1 == psplit.psplit(map(str, range(   1)), bdir="splited")
  assert  1 == psplit.psplit(map(str, range(  16)), bdir="splited")
  assert  2 == psplit.psplit(map(str, range(  17)), bdir="splited")
  assert  2 == psplit.psplit(map(str, range(  32)), bdir="splited")
  assert  3 == psplit.psplit(map(str, range(  33)), bdir="splited")
  assert  3 == psplit.psplit(map(str, range(  48)), bdir="splited")
  assert  4 == psplit.psplit(map(str, range(  49)), bdir="splited")
  assert 16 == psplit.psplit(map(str, range( 256)), bdir="splited")
  assert 64 == psplit.psplit(map(str, range(1024)), bdir="splited")

  assert 1 == psplit.psplit(map(str, range( 256)), bdir="splited", sfunc=functools.partial(psplit.psplit_sfunc, hwm= 8))
  assert 1 == psplit.psplit(map(str, range(1024)), bdir="splited", sfunc=functools.partial(psplit.psplit_sfunc, hwm=10))

  assert 1 == psplit.psplit(range(8), bdir="splited", prefilter=str)
  assert 1 == psplit.psplit(range(8), bdir="splited", prefilter=str, line2tuple=lambda lines: map(lambda line: (0,line), lines))

  i = iter([
    '{"n":"tt", "v": 333}\n',
    '{"n":"st", "v": 634}\n',
    '{"n":"mf", "v":3776}\n',
  ])
  assert 2 == psplit.psplit(i, bdir="splited", prefix="[", suffix="]\n", separator=",", sfunc=functools.partial(psplit.psplit_sfunc, hwm=1))
  with open(os.path.join("splited", "0.txt")) as f: assert f.read() == '[{"n":"tt", "v": 333},{"n":"st", "v": 634}]\n'
  with open(os.path.join("splited", "1.txt")) as f: assert f.read() == '[{"n":"mf", "v":3776}]\n'
  pass
