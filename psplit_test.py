import os

import psplit

def test_psplit_key2name():
  assert os.path.join(".", "0.txt") == psplit.psplit_key2name()
  assert os.path.join(".", "1.txt") == psplit.psplit_key2name(1)
  assert os.path.join("a", "1.txt") == psplit.psplit_key2name(1, "a")
  assert os.path.join("a", "1.csv") == psplit.psplit_key2name(1, "a", ".csv")
