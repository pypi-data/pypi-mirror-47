from duniterpy.key import SecretKey
import unittest


class TestEncryptionKey(unittest.TestCase):
    def test_from_bob_to_alice(self):
        bob_secret_key = SecretKey("bob", "password")
        alice_secret_key = SecretKey("alice", "password")
        text = "Relatively ciphered text"
        noonce = "00005D6FC6E22FB308D8815A565A01C66FFB7DC761D616DE0698F6322565F1D6"[:24]
        bob_to_alice = bob_secret_key.encrypt(alice_secret_key.public_key.base58(), noonce, text)
        alice_from_bob = alice_secret_key.decrypt(bob_secret_key.public_key.base58(), noonce, bob_to_alice)
        self.assertEqual(alice_from_bob, text)
