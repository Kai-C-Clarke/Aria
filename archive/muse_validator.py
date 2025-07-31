#!/usr/bin/env python3
"""
muse_validator.py - MUSE Protocol Expression Validator
Validates MUSE symbolic expressions for syntax, structure, and semantic correctness
Part of the MUSE Protocol (Musical Universal Symbolic Expression) v3.0
"""

import yaml
import re
import sys
from typing import Dict, List, Tuple, Optional, Union
from dataclasses import dataclass

@dataclass
class ValidationResult:
    """Container for validation results"""
    is_valid: bool
    expression: str
    errors: List[str]
    warnings: List[str]
    parsed_components: Optional[Dict] = None

class MuseValidator:
    def __init__(self, schema_path: str = "muse_protocol_v3_schema.yaml"):
        """Initialize MUSE validator with schema file"""
        self.schema_path = schema_path
        self.schema = None
        self.load_schema()
    
    def load_schema(self):
        """Load the MUSE protocol schema"""
        try:
            with open(self.schema_path, 'r') as file:
                self.schema = yaml.safe_load(file)
            print(f"✅ MUSE Schema loaded for validation: v{self.schema.get('schema_version', 'unknown')}")
        except FileNotFoundError:
            print(f"❌ MUSE schema file not found: {self.schema_path}")
            raise
        except yaml.YAMLError as e:
            print(f"❌ Error parsing MUSE schema: {e}")
            raise
    
    def validate_expression_format(self, expression: str) -> Tuple[bool, List[str]]:
        """
        Validate the basic format of a MUSE expression
        Expected format: SYMBOL[+SYMBOL2]_modifier1_modifier2[_modifier3][_REGISTER]
        """
        errors = []
        
        if not expression or not isinstance(expression, str):
            errors.append("Expression must be a non-empty string")
            return False, errors
        
        # Check for invalid characters
        if not re.match(r'^[A-Z0-9+_\.]+$', expression):
            errors.append("Expression contains invalid characters (only A-Z, 0-9, +, _, . allowed)")
        
        # Split by underscore
        parts = expression.split('_')
        if len(parts) < 1:
            errors.append("Expression must contain at least one symbol")
            return False, errors
        
        # Check symbol part (first part)
        symbol_part = parts[0]
        if not symbol_part:
            errors.append("Symbol part cannot be empty")
        elif not re.match(r'^[A-Z]{3}(\+[A-Z]{3})*$', symbol_part):
            errors.append("Symbols must be 3-letter uppercase codes, optionally combined with '+'")
        
        # Check modifier parts (if present)
        modifier_parts = parts[1:]
        
        # Check if last part might be a register
        register_part = None
        if modifier_parts and modifier_parts[-1] in ['L', 'H', 'X']:
            register_part = modifier_parts[-1]
            modifier_parts = modifier_parts[:-1]
        
        # Validate modifier values
        for i, part in enumerate(modifier_parts):
            try:
                value = float(part)
                if not (0.0 <= value <= 1.0):
                    errors.append(f"Modifier {i+1} value '{part}' must be between 0.0 and 1.0")
            except ValueError:
                errors.append(f"Modifier {i+1} value '{part}' is not a valid number")
        
        return len(errors) == 0, errors
    
    def validate_symbols(self, symbols: List[str]) -> Tuple[bool, List[str], List[str]]:
        """Validate that all symbols exist in the schema"""
        errors = []
        warnings = []
        schema_symbols = self.schema.get('symbols', {})
        
        for symbol in symbols:
            if symbol not in schema_symbols:
                errors.append(f"Unknown symbol: '{symbol}' (not found in MUSE schema)")
            else:
                # Check if symbol has valid structure
                symbol_data = schema_symbols[symbol]
                if not symbol_data.get('notes'):
                    warnings.append(f"Symbol '{symbol}' has no notes defined")
        
        return len(errors) == 0, errors, warnings
    
    def validate_modifiers(self, modifiers: List[float]) -> Tuple[bool, List[str], List[str]]:
        """Validate modifier count and ranges"""
        errors = []
        warnings = []
        
        schema_modifiers = self.schema.get('modifiers', {})
        expected_count = len(schema_modifiers)
        
        if len(modifiers) > expected_count:
            errors.append(f"Too many modifiers: got {len(modifiers)}, expected at most {expected_count}")
        elif len(modifiers) < expected_count:
            warnings.append(f"Fewer modifiers than expected: got {len(modifiers)}, schema defines {expected_count}")
        
        # Validate ranges
        for i, value in enumerate(modifiers):
            modifier_names = list(schema_modifiers.keys())
            if i < len(modifier_names):
                mod_name = modifier_names[i]
                mod_range = schema_modifiers[mod_name].get('range', [0.0, 1.0])
                if not (mod_range[0] <= value <= mod_range[1]):
                    errors.append(f"Modifier '{mod_name}' value {value} outside valid range {mod_range}")
        
        return len(errors) == 0, errors, warnings
    
    def validate_register_shift(self, register: str) -> Tuple[bool, List[str], List[str]]:
        """Validate register shift notation"""
        errors = []
        warnings = []
        
        if not register:  # Empty register is valid (no shift)
            return True, errors, warnings
        
        valid_registers = ['L', 'H', 'X']  # From schema: _L, _H, _X
        if register not in valid_registers:
            errors.append(f"Unknown register shift: '{register}' (valid: {valid_registers})")
        
        schema_shifts = self.schema.get('register_shifts', {})
        shift_key = f"_{register}"
        if shift_key not in schema_shifts:
            warnings.append(f"Register shift '_{register}' not defined in schema")
        
        return len(errors) == 0, errors, warnings
    
    def validate_compound_logic(self, symbols: List[str]) -> Tuple[bool, List[str], List[str]]:
        """Validate logical combinations of symbols"""
        errors = []
        warnings = []
        
        if len(symbols) > 4:
            warnings.append(f"Compound expression with {len(symbols)} symbols may be complex to interpret")
        
        # Check for logical conflicts
        if 'SIL' in symbols and len(symbols) > 1:
            warnings.append("Combining SIL (silence) with other symbols may create ambiguous meaning")
        
        if 'BGN' in symbols and 'END' in symbols:
            warnings.append("Combining BGN (beginning) and END (ending) in same expression")
        
        return len(errors) == 0, errors, warnings
    
    def parse_expression(self, expression: str) -> Tuple[List[str], List[float], str]:
        """Parse expression into components (reused from decoder logic)"""
        parts = expression.split('_')
        
        # First part contains symbols
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
                pass  # Will be caught in format validation
        
        return symbols, modifiers, register
    
    def validate(self, expression: str, strict: bool = False) -> ValidationResult:
        """
        Main validation function for MUSE expressions
        
        Args:
            expression: MUSE symbolic expression string
            strict: If True, warnings become errors
            
        Returns:
            ValidationResult with detailed validation info
        """
        errors = []
        warnings = []
        parsed_components = None
        
        try:
            # Step 1: Basic format validation
            is_valid_format, format_errors = self.validate_expression_format(expression)
            errors.extend(format_errors)
            
            if not is_valid_format:
                return ValidationResult(
                    is_valid=False,
                    expression=expression,
                    errors=errors,
                    warnings=warnings
                )
            
            # Step 2: Parse components
            symbols, modifiers, register = self.parse_expression(expression)
            parsed_components = {
                'symbols': symbols,
                'modifiers': modifiers,
                'register': register
            }
            
            # Step 3: Validate symbols
            symbols_valid, symbol_errors, symbol_warnings = self.validate_symbols(symbols)
            errors.extend(symbol_errors)
            warnings.extend(symbol_warnings)
            
            # Step 4: Validate modifiers
            modifiers_valid, modifier_errors, modifier_warnings = self.validate_modifiers(modifiers)
            errors.extend(modifier_errors)
            warnings.extend(modifier_warnings)
            
            # Step 5: Validate register shift
            register_valid, register_errors, register_warnings = self.validate_register_shift(register)
            errors.extend(register_errors)
            warnings.extend(register_warnings)
            
            # Step 6: Validate compound logic
            logic_valid, logic_errors, logic_warnings = self.validate_compound_logic(symbols)
            errors.extend(logic_errors)
            warnings.extend(logic_warnings)
            
            # Step 7: Apply strict mode
            if strict and warnings:
                errors.extend([f"STRICT: {w}" for w in warnings])
                warnings = []
            
            is_valid = len(errors) == 0
            
            return ValidationResult(
                is_valid=is_valid,
                expression=expression,
                errors=errors,
                warnings=warnings,
                parsed_components=parsed_components
            )
            
        except Exception as e:
            errors.append(f"Validation error: {str(e)}")
            return ValidationResult(
                is_valid=False,
                expression=expression,
                errors=errors,
                warnings=warnings,
                parsed_components=parsed_components
            )
    
    def validate_batch(self, expressions: List[str], strict: bool = False) -> List[ValidationResult]:
        """Validate multiple expressions at once"""
        results = []
        for expr in expressions:
            result = self.validate(expr, strict=strict)
            results.append(result)
        return results
    
    def suggest_corrections(self, expression: str) -> List[str]:
        """Suggest corrections for invalid expressions"""
        suggestions = []
        
        # Basic format fixes
        if '_' not in expression and len(expression) > 3:
            suggestions.append(f"Add modifiers: '{expression}_0.5_0.5'")
        
        # Symbol case fixes
        if re.search(r'[a-z]', expression):
            fixed = expression.upper()
            suggestions.append(f"Convert to uppercase: '{fixed}'")
        
        # Common symbol corrections
        symbol_fixes = {
            'FUND': 'FND', 'FOUND': 'FND', 'BASE': 'FND',
            'QUEST': 'INQ', 'QUESTION': 'INQ', 'ASK': 'INQ',
            'RESOLVE': 'RES', 'ANSWER': 'RES', 'END': 'RES',
            'TENSION': 'TNS', 'STRESS': 'TNS', 'CONFLICT': 'TNS'
        }
        
        for wrong, right in symbol_fixes.items():
            if wrong in expression.upper():
                fixed = expression.upper().replace(wrong, right)
                suggestions.append(f"Symbol correction: '{fixed}'")
        
        return suggestions[:3]  # Limit to top 3 suggestions

def main():
    """Test the MUSE validator with example expressions"""
    
    # Test expressions - mix of valid and invalid
    test_expressions = [
        # Valid expressions
        "FND_0.6_0.8",
        "INQ_0.8_0.6_0.7",
        "FND+INQ_0.6_0.8_0.5",
        "TNS+RES_0.9_0.3_0.4",
        "CNT+DEV_0.7_0.5_0.6_H",
        "SIL_0.0_0.0_0.0",
        "BGN_0.3_0.25_0.5_L",
        
        # Invalid expressions (for testing)
        "INVALID_1.5_0.8",          # Invalid symbol, modifier out of range
        "fnd_0.6_0.8",              # Lowercase
        "FND_abc_0.8",              # Invalid modifier
        "FND+UNKNOWN_0.6_0.8",     # Unknown symbol
        "FND_0.6_0.8_0.7_0.5",     # Too many modifiers
        "FND_0.6_0.8_Z",           # Invalid register
        "",                         # Empty expression
    ]
    
    try:
        validator = MuseValidator()
        
        print("🎭 MUSE Protocol Expression Validator Test")
        print("=" * 60)
        
        valid_count = 0
        total_count = len(test_expressions)
        
        for expr in test_expressions:
            print(f"\n🔍 Validating: '{expr}'")
            
            result = validator.validate(expr)
            
            if result.is_valid:
                print(f"   ✅ VALID")
                valid_count += 1
                if result.parsed_components:
                    comp = result.parsed_components
                    print(f"      Symbols: {comp['symbols']}")
                    print(f"      Modifiers: {comp['modifiers']}")
                    if comp['register']:
                        print(f"      Register: {comp['register']}")
            else:
                print(f"   ❌ INVALID")
                for error in result.errors:
                    print(f"      Error: {error}")
                
                # Show suggestions for invalid expressions
                suggestions = validator.suggest_corrections(expr)
                if suggestions:
                    print("      💡 Suggestions:")
                    for suggestion in suggestions:
                        print(f"         {suggestion}")
            
            if result.warnings:
                print("      ⚠️  Warnings:")
                for warning in result.warnings:
                    print(f"         {warning}")
        
        print(f"\n📊 Validation Summary: {valid_count}/{total_count} expressions valid")
    
    except Exception as e:
        print(f"❌ Failed to initialize MUSE validator: {e}")

if __name__ == "__main__":
    main()
