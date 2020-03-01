import os

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
