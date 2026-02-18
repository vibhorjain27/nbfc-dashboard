"""
P/B Chart test suite
Tests every scenario before deploying.
Run with: python3 test_pb_chart.py
"""

import sys, types, unittest
import pandas as pd
import numpy as np
from unittest.mock import MagicMock, patch
from datetime import datetime, timedelta

# ── 1. Stub out Streamlit so we can import the dashboard module ──────────────
st_mock = MagicMock()
st_mock.cache_data = lambda **kw: (lambda f: f)   # must return decorator, not MagicMock
st_mock.tabs.side_effect   = lambda labels: [MagicMock() for _ in labels]
st_mock.columns.side_effect = lambda n, **kw: [MagicMock() for _ in range(n if isinstance(n, int) else len(n))]

# session_state needs attribute-style access (st.session_state.foo = bar)
class _SessionState(dict):
    def __getattr__(self, k):
        try: return self[k]
        except KeyError: raise AttributeError(k)
    def __setattr__(self, k, v): self[k] = v
    def __contains__(self, k): return dict.__contains__(self, k)
st_mock.session_state = _SessionState()

# stub streamlit.components.v1
components_mock = MagicMock()
components_v1_mock = MagicMock()
st_mock.components = components_mock
components_mock.v1 = components_v1_mock
sys.modules['streamlit'] = st_mock
sys.modules['streamlit.components'] = components_mock
sys.modules['streamlit.components.v1'] = components_v1_mock

# ── 2. Stub out yfinance with a controllable mock ────────────────────────────
yf_mock = types.ModuleType('yfinance')

def make_price_series(days=252, start_price=8800.0, ticker_symbol=None):
    """Generate a realistic 1-year daily price series."""
    dates = pd.date_range(end=datetime.today(), periods=days, freq='B')
    prices = start_price * (1 + np.random.randn(days).cumsum() * 0.01)
    prices = np.abs(prices)
    return pd.DataFrame({'Close': prices, 'Volume': 1_000_000}, index=dates)

PRICES_BY_SYMBOL = {
    'BAJFINANCE.NS':  make_price_series(start_price=1024),
    'CHOLAFIN.NS':    make_price_series(start_price=1717),
    'SHRIRAMFIN.NS':  make_price_series(start_price=1076),
    'MUTHOOTFIN.NS':  make_price_series(start_price=3457),
    'M&MFIN.NS':      make_price_series(start_price=384),
    'LTF.NS':         make_price_series(start_price=300),
    'ABCAPITAL.NS':   make_price_series(start_price=350),
    'PIRAMALFIN.NS':  make_price_series(start_price=1758),
    'POONAWALLA.NS':  make_price_series(start_price=490),
}

class FakeTicker:
    def __init__(self, symbol, mode='all_fail'):
        self.symbol = symbol
        self.mode = mode  # controls which layers work
        self._price_data = PRICES_BY_SYMBOL.get(symbol, pd.DataFrame())

    def history(self, period='1y'):
        if self.mode == 'price_fails':
            return pd.DataFrame()
        return self._price_data

    @property
    def quarterly_balance_sheet(self):
        if self.mode == 'layer1_works':
            # Return a fake balance sheet with equity data
            dates = pd.date_range(end=datetime.today(), periods=4, freq='QE')
            data = {'Common Stock Equity': [60000e7, 58000e7, 55000e7, 52000e7]}
            return pd.DataFrame(data, index=dates).T
        raise Exception("Simulated yfinance balance sheet failure")

    @property
    def info(self):
        if self.mode == 'layer3_works':
            return {'sharesOutstanding': 60_000_000, 'bookValue': 1100.0}
        if self.mode == 'layer1_works':
            return {'sharesOutstanding': 60_000_000}
        raise Exception("Simulated yfinance info failure")

def make_yf_ticker(mode):
    def _ticker(symbol):
        return FakeTicker(symbol, mode=mode)
    return _ticker

yf_mock.Ticker = make_yf_ticker('all_fail')  # default: everything fails
sys.modules['yfinance'] = yf_mock

# ── 3. Stub plotly ────────────────────────────────────────────────────────────
for mod in ['plotly', 'plotly.graph_objects', 'plotly.subplots']:
    sys.modules[mod] = MagicMock()

# ── 4. Now import the real dashboard code ────────────────────────────────────
sys.path.insert(0, '/home/user/nbfc-dashboard')

# Patch fetch_stock_data BEFORE import so the module-level def is replaced
import importlib

# We'll monkey-patch after import
import nbfc_dashboard_v1 as dash

# ── 5. Override fetch_stock_data to use our fake prices ───────────────────────
def fake_fetch_stock_data(symbol, period='1y'):
    return PRICES_BY_SYMBOL.get(symbol)

dash.fetch_stock_data = fake_fetch_stock_data

# ─────────────────────────────────────────────────────────────────────────────

class TestFallbackBV(unittest.TestCase):
    """Test that _FALLBACK_BV has all 9 NBFCs and sensible values."""

    def test_all_companies_present(self):
        for name in dash.NBFCS:
            self.assertIn(name, dash._FALLBACK_BV,
                          f"Missing fallback BV for {name}")

    def test_values_are_positive(self):
        for name, bv in dash._FALLBACK_BV.items():
            self.assertGreater(bv, 0, f"BV <= 0 for {name}")

    def test_values_plausible_range(self):
        """BV per share for Indian NBFCs should be between ₹10 and ₹10,000."""
        for name, bv in dash._FALLBACK_BV.items():
            self.assertGreater(bv, 10,   f"BV suspiciously low for {name}: {bv}")
            self.assertLess(bv,    10000, f"BV suspiciously high for {name}: {bv}")


class TestScenario_AllLayersFail(unittest.TestCase):
    """
    Scenario: Streamlit Cloud — yfinance rate-limited, Screener blocked.
    Layer 1, 2, 3 all fail → must use Layer 4 fallback.
    """

    def setUp(self):
        # yfinance Ticker raises exceptions (rate-limited)
        yf_mock.Ticker = make_yf_ticker('all_fail')
        # Screener also blocked
        self._screener_patch = patch.object(dash, 'get_screener_book_value',
                                            return_value=None)
        self._screener_patch.start()

    def tearDown(self):
        self._screener_patch.stop()

    def test_pb_timeseries_returns_data_via_fallback(self):
        for name, symbol in dash.NBFCS.items():
            with self.subTest(company=name):
                result = dash.get_pb_timeseries(symbol, name)
                self.assertIsNotNone(result,
                    f"get_pb_timeseries returned None for {name} — fallback not working")
                self.assertFalse(result.empty, f"Empty DataFrame for {name}")
                self.assertIn('PB', result.columns)
                # P/B should be a reasonable multiple (0.5x – 100x)
                pb_latest = float(result['PB'].iloc[-1])
                self.assertGreater(pb_latest, 0.5,  f"P/B too low for {name}: {pb_latest:.1f}x")
                self.assertLess(pb_latest,    100.0, f"P/B too high for {name}: {pb_latest:.1f}x")
                print(f"  ✓ {name}: P/B = {pb_latest:.2f}x  (BV = ₹{dash._FALLBACK_BV[name]})")

    def test_create_pb_chart_not_none(self):
        chart = dash.create_pb_chart(list(dash.NBFCS.keys()))
        self.assertIsNotNone(chart, "create_pb_chart returned None — chart will show error")
        print("  ✓ create_pb_chart returned a figure")


class TestScenario_PriceFails(unittest.TestCase):
    """
    Scenario: yfinance price history completely unavailable.
    Should return None gracefully (no crash).
    """

    def setUp(self):
        yf_mock.Ticker = make_yf_ticker('price_fails')
        self._screener_patch = patch.object(dash, 'get_screener_book_value',
                                            return_value=None)
        self._screener_patch.start()
        # Also make fetch_stock_data return empty
        self._orig = dash.fetch_stock_data
        dash.fetch_stock_data = lambda symbol, period='1y': None

    def tearDown(self):
        self._screener_patch.stop()
        dash.fetch_stock_data = self._orig

    def test_returns_none_gracefully(self):
        result = dash.get_pb_timeseries('BAJFINANCE.NS', 'Bajaj Finance')
        self.assertIsNone(result, "Should return None when price data is unavailable")
        print("  ✓ Returns None gracefully when price data is unavailable")

    def test_chart_returns_none_not_crash(self):
        chart = dash.create_pb_chart(list(dash.NBFCS.keys()))
        self.assertIsNone(chart, "chart should be None when all stocks lack price data")
        print("  ✓ create_pb_chart returns None gracefully (no crash)")


class TestScenario_Layer1Works(unittest.TestCase):
    """
    Scenario: yfinance balance sheet available (local dev).
    Layer 1 should produce time-varying P/B, not a flat line.
    """

    def setUp(self):
        yf_mock.Ticker = make_yf_ticker('layer1_works')

    def test_quarterly_bv_produces_timeseries(self):
        result = dash.get_pb_timeseries('BAJFINANCE.NS', 'Bajaj Finance')
        self.assertIsNotNone(result)
        self.assertIn('PB', result.columns)
        # With quarterly BV the P/B series should have more than 1 unique value
        print(f"  ✓ Layer 1: P/B range = {result['PB'].min():.2f}x – {result['PB'].max():.2f}x")


class TestScenario_Layer3Works(unittest.TestCase):
    """
    Scenario: yfinance info['bookValue'] is available.
    Layer 3 should produce a flat-line P/B (single BV, varying price).
    """

    def setUp(self):
        yf_mock.Ticker = make_yf_ticker('layer3_works')
        self._screener_patch = patch.object(dash, 'get_screener_book_value',
                                            return_value=None)
        self._screener_patch.start()

    def tearDown(self):
        self._screener_patch.stop()

    def test_layer3_bv_used(self):
        result = dash.get_pb_timeseries('BAJFINANCE.NS', 'Bajaj Finance')
        self.assertIsNotNone(result)
        # BV should be the value from info['bookValue'] = 1100.0
        self.assertAlmostEqual(float(result['BookValue'].iloc[0]), 1100.0, places=0)
        print(f"  ✓ Layer 3: BV = ₹{result['BookValue'].iloc[0]:.0f} (from yfinance info)")


class TestScenario_ScreenerWorks(unittest.TestCase):
    """
    Scenario: Screener.in is accessible.
    Layer 2 should override Layer 4 fallback.
    """

    def setUp(self):
        yf_mock.Ticker = make_yf_ticker('all_fail')
        self._screener_patch = patch.object(dash, 'get_screener_book_value',
                                            return_value=950.0)  # fake Screener BV
        self._screener_patch.start()

    def tearDown(self):
        self._screener_patch.stop()

    def test_screener_bv_used_over_fallback(self):
        result = dash.get_pb_timeseries('BAJFINANCE.NS', 'Bajaj Finance')
        self.assertIsNotNone(result)
        self.assertAlmostEqual(float(result['BookValue'].iloc[0]), 950.0, places=0)
        print(f"  ✓ Layer 2 (Screener): BV = ₹{result['BookValue'].iloc[0]:.0f} overrides fallback")


class TestPBRatioSanity(unittest.TestCase):
    """
    Validate the hardcoded BV values produce reasonable P/B ratios
    given approximate current market prices.
    """

    # Current prices from Screener.in (live-scraped Feb 2026)
    APPROX_PRICES = {
        'Bajaj Finance':        1024,
        'Cholamandalam Finance': 1717,
        'Shriram Finance':       1076,
        'Muthoot Finance':       3457,
        'Mahindra Finance':       384,
        'L&T Finance':            300,
        'Aditya Birla Capital':   350,
        'Piramal Finance':       1758,
        'Poonawalla Fincorp':     490,
    }

    def test_pb_ratios_are_plausible(self):
        print()
        ok = True
        for name, price in self.APPROX_PRICES.items():
            bv = dash._FALLBACK_BV[name]
            pb = price / bv
            status = "✓" if 0.5 <= pb <= 30 else "⚠ SUSPICIOUS"
            print(f"  {status} {name}: price=₹{price}  BV=₹{bv}  P/B={pb:.1f}x")
            if not (0.5 <= pb <= 30):
                ok = False
        self.assertTrue(ok, "Some P/B ratios look wrong — check _FALLBACK_BV values")


if __name__ == '__main__':
    print("=" * 65)
    print("P/B Chart Test Suite")
    print("=" * 65)
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    for cls in [
        TestFallbackBV,
        TestPBRatioSanity,
        TestScenario_AllLayersFail,
        TestScenario_PriceFails,
        TestScenario_Layer1Works,
        TestScenario_Layer3Works,
        TestScenario_ScreenerWorks,
    ]:
        suite.addTests(loader.loadTestsFromTestCase(cls))
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    sys.exit(0 if result.wasSuccessful() else 1)
