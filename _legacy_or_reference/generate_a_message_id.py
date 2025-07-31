python3 -c "
import sys
sys.path.append('.')
exec(open('midi64_clean_hex_suite.py').read())
generator = HexIDGenerator()
print('First Claude message:', generator.get_next_id('Claude', 'A'))
print('First Kai message:', generator.get_next_id('Kai', 'A'))
"