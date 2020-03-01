import os

import psplit

def test_psplit_key2name():
  assert os.path.join(".", "0.txt") == psplit.psplit_key2name()
