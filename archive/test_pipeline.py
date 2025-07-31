# In your Aria directory, create a simple test file:
# test_pipeline.py

from symbolic_pipeline import process_exchange

# Use real MIDI64 from our previous exchanges
test_midi64 = "TVRoZAAAAAYAAQABAeBNVHJrAAAANwD/UQMHoSAA/1gEBAIYCACwAUwAsEplALALPwCQPGRggDwAYJBAZGCAQABgkENkYIBDAAD/LwA="

result = process_exchange(test_midi64, "TEST_K2C_00001")
print("🎵 Symbolic Analysis:", result['symbolic_tags'])
print("💭 Poetic Reflection:", result['poetic_reflection'])
print("📁 Files saved to:", "./exchange_logs/TEST_K2C_00001/")