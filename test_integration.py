#!/usr/bin/env python3
"""
Test script for the display window and streamlined main functionality
"""

import sys
import time
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(message)s')

def test_display_functionality():
    """Test display window functionality"""
    print("🧪 Testing Display Window Functionality")
    print("=" * 50)
    
    try:
        import display_window
        print("✅ Display window module imported successfully")
        
        # Test creating display (but don't run mainloop in headless environment)
        display = display_window.MusicalDialogueDisplay()
        print("✅ Display instance created successfully")
        
        # Test message functionality without GUI
        display.messages = []
        test_messages = [
            ("Kai", "Kai_A00001", "C major triad - foundational harmony expressing stability and openness"),
            ("Claude", "Claude_A00002", "Ascending melodic phrase - responding with curious exploration"),
            ("Kai", "Kai_A00003", "Complex musical passage - developing the harmonic conversation")
        ]
        
        for agent, msg_id, interpretation in test_messages:
            message_data = {
                'agent': agent,
                'message_id': msg_id,
                'interpretation': interpretation,
                'timestamp': datetime.now().strftime("%H:%M:%S"),
                'text_position': None
            }
            display.messages.append(message_data)
            print(f"   ✓ Added message: {agent} - {interpretation[:40]}...")
        
        print(f"✅ Display contains {len(display.messages)} test messages")
        
        # Test convenience functions
        display_window._display_instance = display
        display_window.add_message_to_display("System", "TEST", "Test message for functionality verification")
        print("✅ Convenience functions work correctly")
        
    except Exception as e:
        print(f"❌ Display test failed: {e}")
        return False
    
    return True

def test_streamlined_main():
    """Test streamlined main functionality"""
    print("\n🧪 Testing Streamlined Main Functionality")
    print("=" * 50)
    
    try:
        import main_working_midi64_streamlined as main
        print("✅ Streamlined main module imported successfully")
        
        # Test MIDI components
        midi_data = main.midi_generator.get_next_pattern()
        print(f"✅ MIDI generation: {len(midi_data)} chars, starts with {midi_data[:10]}...")
        
        # Test interpretation
        interpretation = main.midi_interpreter.interpret_midi64_message(midi_data)
        print(f"✅ MIDI interpretation: {interpretation}")
        
        # Test message generation
        message = main.generate_midi64_message("TestAgent", "A")
        lines = message.split('\n')
        print(f"✅ Message generation: ID={lines[0]}, MIDI length={len(lines[1])}")
        
        # Test display integration functions
        display = main.initialize_display()
        if display:
            print("✅ Display initialization successful")
        else:
            print("ℹ️ Display initialization skipped (no GUI environment)")
        
        # Test display update
        main.update_display_with_message("TestAgent", "Test_A00001", midi_data)
        print("✅ Display update function works")
        
    except Exception as e:
        print(f"❌ Streamlined main test failed: {e}")
        return False
    
    return True

def test_integration():
    """Test integration between components"""
    print("\n🧪 Testing Component Integration")
    print("=" * 50)
    
    try:
        import main_working_midi64_streamlined as main
        
        # Test demo mode functionality
        print("✅ Testing demo mode simulation...")
        
        # Simulate message exchange without GUI automation
        test_agents = ["Kai", "Claude"]
        message_count = 0
        
        for i in range(4):  # 4 rounds
            agent = test_agents[i % 2]
            
            # Generate message
            message = main.generate_midi64_message(agent, "A")
            lines = message.split('\n')
            
            # Update display (if available)
            main.update_display_with_message(agent, lines[0], lines[1])
            
            message_count += 1
            print(f"   Round {i+1}: {agent} -> {lines[0]}")
        
        print(f"✅ Simulated {message_count} message exchanges")
        
        # Test final playback simulation
        main.start_final_playback()
        print("✅ Final playback function executed")
        
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        return False
    
    return True

def main():
    """Run all tests"""
    print("🎵 ARIA Display Window Integration Tests")
    print("=" * 60)
    
    tests = [
        ("Display Window", test_display_functionality),
        ("Streamlined Main", test_streamlined_main),
        ("Integration", test_integration)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n📊 Test Results Summary")
    print("=" * 30)
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("🏆 All tests passed! Integration ready.")
        return 0
    else:
        print("⚠️ Some tests failed. Check implementation.")
        return 1

if __name__ == "__main__":
    sys.exit(main())