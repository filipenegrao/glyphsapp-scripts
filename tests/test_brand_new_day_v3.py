import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'workflow'))

import importlib, types

# Stub out Glyphs so the module imports without crashing
glyphs_stub = types.ModuleType('Glyphs')
sys.modules.setdefault('Glyphs', glyphs_stub)

import brand_new_day_v3 as bnd


def test_strip_date_removes_trailing_date():
    assert bnd.strip_date_from_name("MyFont 2026-05-20") == "MyFont"

def test_strip_date_leaves_undated_name():
    assert bnd.strip_date_from_name("MyFont") == "MyFont"

def test_strip_date_handles_multiple_words():
    assert bnd.strip_date_from_name("My Font Display 2025-01-01") == "My Font Display"

def test_today_str_format():
    import re
    assert re.match(r'\d{4}-\d{2}-\d{2}', bnd.today_str())
