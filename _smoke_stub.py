"""Smoke harness: run the dashboard with yfinance stubbed out."""
import sys, types
import pandas as pd

fake = types.ModuleType('yfinance')

class _Ticker:
    def __init__(self, *a, **k): pass
    def history(self, *a, **k): return pd.DataFrame()
    @property
    def fast_info(self): return types.SimpleNamespace(shares=None, market_cap=None)

fake.Ticker = _Ticker
fake.download = lambda *a, **k: None
sys.modules['yfinance'] = fake

exec(compile(open('nbfc_dashboard_v1.py', encoding='utf-8').read(), 'nbfc_dashboard_v1.py', 'exec'))
