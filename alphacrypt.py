letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
import random
random.seed()
def alpha2ord(s):
    result = []
    for c in s:
        c = c.upper()
        try:
            result.append(letters.find(c))
        except:
            pass
    return result
def ord2alpha(ords):
    result = ''
    for o in ords:
        result += letters[o]
    return result

def pt2ct(pt, keystream):
    if len(keystream) != len(pt):
        raise Exception('Unequal PT and Keystream')
    pt_ord = alpha2ord(pt)
    kt_ord = alpha2ord(keystream)
    ct_ord = []
    for i in range(len(pt_ord)):
        ct_ord.append((pt_ord[i] + kt_ord[i]) % 26)
    return ord2alpha(ct_ord)

def ct2pt(ct, keystream):
    if len(keystream) != len(ct):
        raise Exception('Unequal CT and Keystream')
    ct_ord = alpha2ord(ct)
    kt_ord = alpha2ord(keystream)
    pt_ord = []
    for i in range(len(ct_ord)):
        pt_ord.append((ct_ord[i] - kt_ord[i]) % 26)
    return ord2alpha(pt_ord)

def rand_iv(size = 10):
    result = ''

    for i in range(size):
        result += random.choice(letters)
    return result

class Cipher(object):
    def __init__(self, key, iv):
        pass
    def get_next_char(self):
        raise Exception('Not impmlemented')
    def get_n_chars(self, n):
        result = ''
        for i in range(n):
            result += self.get_next_char()
        return result

class NullCipher(Cipher):
    def __init__(self, key, iv):
        super(NullCipher, self).__init__(key, iv)

    def get_next_char(self):
        return 'A'
def filter(msg):
    result = ''
    for c in msg:
        c = c.upper()
        if c in letters:
            result += c
    return result
class Cryptor:
    def __init__(self, key, iv_size = 10):
        self.key = key
        self.iv_size = iv_size

    def encrypt(self, pt):
        pt = filter(pt)
        iv = rand_iv(self.iv_size)
        cipher = NullCipher(self.key, iv)
        keystream = cipher.get_n_chars(len(pt))
        return iv + pt2ct(pt, keystream)

    def decrypt(self, msg):
        msg = filter(msg)
        iv = msg[:self.iv_size]
        ct = msg[self.iv_size:]
        cipher = NullCipher(self.key, iv)
        keystream = cipher.get_n_chars(len(ct))
        return ct2pt(ct, keystream)

def groups(msg, groupsize = 5):
    i = 0
    results = []
    while i < len(msg):
        group = msg[i:i+5]
        i += 5
        results.append(group)
    return results

def self_test(verbose = False):
    test_msg = 'The quick brown fox jumped over the lazy dog'
    expected_pt = 'THEQUICKBROWNFOXJUMPEDOVERTHELAZYDOG'
    cryptor = Cryptor('TESTKEY')
    ct = cryptor.encrypt(test_msg)
    pt = cryptor.decrypt(ct)
    if verbose:
        print 'Test MSG: %s' % test_msg
        print 'Cipher T: %s' % ' '.join(groups(ct))
        print 'Plain  T: %s' % pt
        print 'Expected: %s' % expected_pt
        if expected_pt == pt:
            print 'PASS!'
    if pt != expected_pt:
        raise Exception('Decrypt does not match expected')
self_test(verbose=True)
