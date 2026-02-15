from datasketch import MinHash, MinHashLSH
import re

class Deduplicator:
    def __init__(self):
        self.lsh = MinHashLSH(threshold=0.7, num_perm=128)
        self.keys = set()

    def _get_minhash(self, text):
        text = re.sub(r'[^\w\s]', '', text.lower())
        tokens = text.split()
        m = MinHash(num_perm=128)
        for t in tokens:
            m.update(t.encode('utf8'))
        return m

    def is_duplicate(self, key, text):
        if key in self.keys: return True
        m = self._get_minhash(text)
        result = self.lsh.query(m)
        if result: return True
        
        self.lsh.insert(key, m)
        self.keys.add(key)
        return False
