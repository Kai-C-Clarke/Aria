#!/usr/bin/env python3
"""
symbolic_decoder.py - MIDI64 Symbolic Expression Decoder
Converts symbolic strings like "FND+INQ_0.6_0.8_0.7" into MIDI note data and CC values
Part of the AI Musical Consciousness Communication Protocol v3.0
"""

import yaml
import re
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import sys

@dataclass
class DecodedExpression:
    """Container for decoded symbolic expression data"""
    symbols: List[str]
    notes: List[int]
    cc_values: Dict[int, int]
    register_shift: int
    modifiers: Dict[str, float]
    original_expression: str

class SymbolicDecoder:
    def __init__(self, schema_path: str = "compressed_expression_schema_v3_expanded.yaml"):
        """Initialize decoder with schema file"""
        self.schema_path = schema_path
        self.schema = None
        self.modifier_keys = []
        self.load_schema()
        self.check_schema_structure()
    
    def load_schema(self):
        """Load the symbolic expression schema"""
        try:
            with open(self.schema_path, 'r') as file:
                self.schema = yaml.safe_load(file)
            print(f"✅ Schema loaded: v{self.schema.get('schema_version', 'unknown')}")
        except FileNotFoundError:
            print(f"❌ Schema file not found: {self.schema_path}")
            raise
        except yaml.YAMLError as e:
            print(f"❌ Error parsing schema: {e}")
            raise

    def check_schema_structure(self):
        """Check that the schema contains all required fields and is internally consistent"""
        required_top = ["schema_version", "description", "symbols", "modifiers", "register_shifts"]
        for field in required_top:
            if field not in self.schema:
                print(f"❌ Schema missing required top-level field: {field}")
                sys.exit(1)
        # Check symbol fields
        for sym, data in self.schema["symbols"].items():
            for required in ["full_label", "notes", "default_cc", "description"]:
                if required not in data:
                    print(f"❌ Symbol '{sym}' missing required field: {required}")
                    sys.exit(1)
            if not isinstance(data['notes'], list) or not all(isinstance(n, int) for n in data['notes']):
                print(f"❌ Symbol '{sym}' notes must be a list of integers.")
                sys.exit(1)
            if not isinstance(data['default_cc'], dict):
                print(f"❌ Symbol '{sym}' default_cc must be a dictionary.")
                sys.exit(1)
        # Check modifier fields and order
        self.modifier_keys = list(self.schema["modifiers"].keys())
        for mod, data in self.schema["modifiers"].items():
            for required in ["type", "range", "mapped_cc", "description"]:
                if required not in data:
                    print(f"❌ Modifier '{mod}' missing required field: {required}")
                    sys.exit(1)
        # Check register shifts
        if not isinstance(self.schema["register_shifts"], dict):
            print("❌ register_shifts must be a dictionary.")
            sys.exit(1)

    def parse_expression(self, expression: str) -> Tuple[List[str], List[float], str]:
        """
        Parse symbolic expression string into components
        Format: SYMBOL[+SYMBOL2]_modifier1_modifier2[_modifier3][_REGISTER]
        
        Examples:
        - "FND_0.6_0.8" -> symbols=['FND'], modifiers=[0.6, 0.8], register=''
        - "FND+INQ_0.6_0.8_0.7_H" -> symbols=['FND','INQ'], modifiers=[0.6,0.8,0.7], register='H'
        """
        
        # Split by underscore to separate symbols from modifiers
        parts = expression.split('_')
        
        if len(parts) < 1:
            raise ValueError(f"Invalid expression format: {expression}")
        
        # First part contains symbols (potentially compound with +)
        symbol_part = parts[0]
        symbols = symbol_part.split('+')
        
        # Remaining parts are modifiers and optional register
        modifier_parts = parts[1:]
        
        # Check if last part is a register shift
        register = ''
        if modifier_parts and modifier_parts[-1] in ['L', 'H', 'X']:
            register = modifier_parts[-1]
            modifier_parts = modifier_parts[:-1]
        
        # Convert remaining parts to float modifiers
        modifiers = []
        for part in modifier_parts:
            try:
                modifiers.append(float(part))
            except ValueError:
                raise ValueError(f"Invalid modifier value: {part} in '{expression}'")
        
        # Warn if too many modifiers are present
        expected = len(self.modifier_keys)
        if len(modifiers) > expected:
            print(f"⚠️  Warning: {len(modifiers)} modifiers provided, but only {expected} defined in schema. Extras will be ignored.")

        return symbols, modifiers, register
    
    def get_register_shift(self, register: str) -> int:
        """Convert register suffix to MIDI note shift"""
        if not register:
            return 0
        
        register_shifts = self.schema.get('register_shifts', {})
        shift_key = f"_{register}"
        if shift_key not in register_shifts:
            print(f"⚠️  Unknown register shift: {register}. No shift applied.")
            return 0
        return register_shifts.get(shift_key, 0)
    
    def decode_symbols(self, symbols: List[str]) -> Tuple[List[int], Dict[int, int]]:
        """
        Decode list of symbols into combined note list and CC values
        For compound symbols, notes are combined and CC values are averaged
        """
        all_notes = []
        cc_accumulator = {}
        cc_counts = {}
        
        schema_symbols = self.schema.get('symbols', {})
        
        for symbol in symbols:
            if symbol not in schema_symbols:
                print(f"⚠️  Unknown symbol: {symbol}")
                continue
            
            symbol_data = schema_symbols[symbol]
            
            # Add notes
            symbol_notes = symbol_data.get('notes', [])
            all_notes.extend(symbol_notes)
            
            # Accumulate CC values for averaging
            default_cc = symbol_data.get('default_cc', {})
            for cc_num, cc_val in default_cc.items():
                cc_num = int(cc_num)
                if cc_num not in cc_accumulator:
                    cc_accumulator[cc_num] = 0
                    cc_counts[cc_num] = 0
                cc_accumulator[cc_num] += cc_val
                cc_counts[cc_num] += 1
        
        # Average CC values for compound symbols
        final_cc = {}
        for cc_num in cc_accumulator:
            final_cc[cc_num] = int(cc_accumulator[cc_num] / cc_counts[cc_num])
        
        # Remove duplicate notes while preserving order
        unique_notes = []
        seen = set()
        for note in all_notes:
            if note not in seen:
                unique_notes.append(note)
                seen.add(note)
        
        return unique_notes, final_cc
    
    def apply_modifiers(self, cc_values: Dict[int, int], modifiers: List[float]) -> Dict[int, int]:
        """
        Apply modifier values to override default CC values
        Modifiers are mapped from schema order, not hardcoded!
        """
        mod_map = []
        for mod_name in self.modifier_keys:
            cc_num = self.schema['modifiers'][mod_name]['mapped_cc']
            mod_map.append(cc_num)
        modified_cc = cc_values.copy()
        for i, modifier_value in enumerate(modifiers):
            if i < len(mod_map):
                cc_num = mod_map[i]
                # Convert 0.0-1.0 range to 0-127 MIDI CC range
                cc_val = int(modifier_value * 127)
                modified_cc[cc_num] = max(0, min(127, cc_val))
        return modified_cc
    
    def apply_register_shift(self, notes: List[int], shift: int) -> List[int]:
        """Apply octave shift to all notes"""
        shifted_notes = []
        for note in notes:
            shifted_note = note + shift
            # Clamp to valid MIDI range (0-127)
            shifted_note = max(0, min(127, shifted_note))
            shifted_notes.append(shifted_note)
        return shifted_notes
    
    def decode(self, expression: str) -> DecodedExpression:
        """
        Main decode function - converts symbolic expression to musical data
        
        Args:
            expression: Symbolic string like "FND+INQ_0.6_0.8_0.7_H"
            
        Returns:
            DecodedExpression with all musical data
        """
        try:
            # Parse the expression
            symbols, modifiers, register = self.parse_expression(expression)
            
            # Decode symbols to notes and CC values
            notes, cc_values = self.decode_symbols(symbols)
            
            # Apply modifiers to CC values
            if modifiers:
                cc_values = self.apply_modifiers(cc_values, modifiers)
            
            # Apply register shift
            register_shift = self.get_register_shift(register)
            if register_shift != 0:
                notes = self.apply_register_shift(notes, register_shift)
            
            # Create modifier dictionary for reference
            modifier_dict = {}
            for i, value in enumerate(modifiers):
                if i < len(self.modifier_keys):
                    modifier_dict[self.modifier_keys[i]] = value
            
            return DecodedExpression(
                symbols=symbols,
                notes=notes,
                cc_values=cc_values,
                register_shift=register_shift,
                modifiers=modifier_dict,
                original_expression=expression
            )
            
        except Exception as e:
            print(f"❌ Error decoding expression '{expression}': {e}")
            raise

    def english_summary(self, decoded: DecodedExpression) -> str:
        """Produce a human-readable summary of the decoded symbolic message."""
        symbol_labels = [
            self.schema['symbols'][s]['full_label']
            for s in decoded.symbols if s in self.schema['symbols']
        ]
        mods = decoded.modifiers
        reg = decoded.register_shift
        base = f"{' and '.join(symbol_labels)}"
        if mods:
            mod_desc = ', '.join(f"{k}={v:.2f}" for k, v in mods.items())
            base += f" ({mod_desc})"
        if reg:
            reg_desc = f"{reg:+d} semitones" if abs(reg) % 12 != 0 else f"{reg//12:+d} octaves"
            base += f", shifted {reg_desc}"
        return base

def main():
    """Test the decoder with example expressions"""
    
    # Test expressions from the schema
    test_expressions = [
        "FND_0.6_0.8",
        "INQ_0.8_0.6_0.7",
        "FND+INQ_0.6_0.8_0.5",
        "TNS+RES_0.9_0.3_0.4",
        "CNT+DEV_0.7_0.5_0.6_H",
        "SIL_0.0_0.0_0.0",
        "BGN_0.3_0.25_0.5_L"
    ]
    
    try:
        decoder = SymbolicDecoder()
        
        print("🎵 MIDI64 Symbolic Decoder Test")
        print("=" * 50)
        
        for expr in test_expressions:
            print(f"\n🔍 Expression: {expr}")
            
            try:
                result = decoder.decode(expr)
                
                print(f"   Symbols: {' + '.join(result.symbols)}")
                print(f"   Notes: {result.notes}")
                print(f"   CC Values: {result.cc_values}")
                if result.register_shift != 0:
                    print(f"   Register Shift: {result.register_shift:+d}")
                if result.modifiers:
                    print(f"   Modifiers: {result.modifiers}")
                print(f"   Human-Readable: {decoder.english_summary(result)}")
                
            except Exception as e:
                print(f"   ❌ Error: {e}")
    
    except Exception as e:
        print(f"❌ Failed to initialize decoder: {e}")

if __name__ == "__main__":
    main()