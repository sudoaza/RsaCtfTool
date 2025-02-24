#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from attacks.abstract_attack import AbstractAttack
from lib.keys_wrapper import PrivateKey
from lib.exceptions import FactorizationError
from lib.number_theory import isqrt, is_square, cuberoot, gcd


def hart(N):
  """ 
  Hart's one line attack 
  taken from wagstaff the joy of factoring
  """
  m = 2
  i = 1
  while not is_square(m):
    s = isqrt(N * i) + 1
    m = pow(s, 2, N)
    i += 1
  t = isqrt(m)
  g = gcd(s - t, N)
  return g, N // g


class Attack(AbstractAttack):
    def __init__(self, timeout=60):
        super().__init__(timeout)
        self.speed = AbstractAttack.speed_enum["medium"]

        
    def attack(self, publickey, cipher=[], progress=True):
        """Run Hart's attack with a timeout"""
        try:
            publickey.p, publickey.q = hart(publickey.n)

        except FactorizationError:
            self.logger.info("N should not be a 4k+2 number...")
            return None, None

        if publickey.p is not None and publickey.q is not None:
            try:
                priv_key = PrivateKey(
                    n=publickey.n,
                    p=int(publickey.p),
                    q=int(publickey.q),
                    e=int(publickey.e),
                )
                return priv_key, None
            except ValueError:
                return None, None

        return None, None

    def test(self):
        from lib.keys_wrapper import PublicKey

        key_data = """-----BEGIN PUBLIC KEY-----
MIGbMA0GCSqGSIb3DQEBAQUAA4GJADCBhQJ+AgAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAnUAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAG+BAgMBAAE=
-----END PUBLIC KEY-----"""
        result = self.attack(PublicKey(key_data), progress=False)
        return result != (None, None)
