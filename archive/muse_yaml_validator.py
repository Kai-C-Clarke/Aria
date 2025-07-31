#!/usr/bin/env python3
"""
muse_yaml_validator.py - Validator for MUSE Protocol YAML Schema v3.x

Checks structure, types, and some semantics for the MUSE symbolic music exchange schema.
"""

import yaml
import sys

REQUIRED_TOP_LEVEL = ["schema_version", "description", "symbols", "modifiers", "register_shifts"]
REQUIRED_SYMBOL_FIELDS = ["full_label", "notes", "default_cc", "description"]
REQUIRED_MODIFIER_FIELDS = ["type", "range", "mapped_cc", "description"]

def error(msg):
    print(f"❌ {msg}")
    sys.exit(1)

def validate_symbol(symbol_key, symbol):
    for field in REQUIRED_SYMBOL_FIELDS:
        if field not in symbol:
            error(f"Symbol '{symbol_key}' missing required field '{field}'")
    if not isinstance(symbol["notes"], list) or not all(isinstance(x, int) for x in symbol["notes"]):
        error(f"Symbol '{symbol_key}': 'notes' must be a list of integers")
    if not isinstance(symbol["default_cc"], dict):
        error(f"Symbol '{symbol_key}': 'default_cc' must be a dictionary")
    for cc, val in symbol["default_cc"].items():
        try:
            cc_num = int(cc)
            if not (0 <= cc_num <= 127):
                error(f"Symbol '{symbol_key}': 'default_cc' key {cc} out of 0-127 range")
            if not (0 <= int(val) <= 127):
                error(f"Symbol '{symbol_key}': 'default_cc' value {val} out of 0-127 range")
        except Exception:
            error(f"Symbol '{symbol_key}': 'default_cc' key/val not integer ({cc}: {val})")

def validate_modifier(mod_key, mod):
    for field in REQUIRED_MODIFIER_FIELDS:
        if field not in mod:
            error(f"Modifier '{mod_key}' missing required field '{field}'")
    if mod["type"] not in {"float", "int", "string"}:
        error(f"Modifier '{mod_key}': 'type' should be one of float, int, string")
    rng = mod["range"]
    if not (isinstance(rng, list) and len(rng) == 2 and all(isinstance(x, (int, float)) for x in rng)):
        error(f"Modifier '{mod_key}': 'range' must be a two-item list of numbers")
    if not (0.0 <= rng[0] <= rng[1] <= 1.0):
        error(f"Modifier '{mod_key}': 'range' values must be between 0.0 and 1.0")
    if not isinstance(mod["mapped_cc"], int):
        error(f"Modifier '{mod_key}': 'mapped_cc' must be an integer")

def validate_register_shifts(rshifts):
    for key, val in rshifts.items():
        if not key.startswith("_"):
            error(f"Register shift key '{key}' must start with '_'")
        if not isinstance(val, int):
            error(f"Register shift '{key}' value must be integer (got {val})")

def main():
    if len(sys.argv) < 2:
        print("Usage: muse_yaml_validator.py <schema.yaml>")
        sys.exit(1)
    path = sys.argv[1]
    with open(path, "r") as f:
        try:
            schema = yaml.safe_load(f)
        except Exception as e:
            error(f"YAML parse error: {e}")
    # Check top-level fields
    for field in REQUIRED_TOP_LEVEL:
        if field not in schema:
            error(f"Top-level field '{field}' missing")
    # Check symbols
    syms = schema["symbols"]
    if not isinstance(syms, dict) or not syms:
        error("Top-level 'symbols' must be a non-empty dictionary")
    for sym_key, sym in syms.items():
        validate_symbol(sym_key, sym)
    # Check modifiers
    mods = schema["modifiers"]
    if not isinstance(mods, dict) or not mods:
        error("Top-level 'modifiers' must be a non-empty dictionary")
    for mod_key, mod in mods.items():
        validate_modifier(mod_key, mod)
    # Check register shifts
    validate_register_shifts(schema["register_shifts"])
    print(f"✅ {path}: Schema version {schema.get('schema_version', '?')} is valid!")
    print(f"✔ {len(syms)} symbol(s), {len(mods)} modifier(s), {len(schema['register_shifts'])} register shifts.")

if __name__ == "__main__":
    main()