# Q4FY26 earnings call transcript data
# Sources: investor call transcripts ingested May 2026
# Structure per NBFC:
#   call_date        : earnings call date
#   management       : key speakers
#   metric_comments  : metric_key → paraphrased management commentary
#   guidance         : FY27 forward guidance bullets
#   swot_prepend     : transcript-sourced S/W/O/T items (prepended to auto-generated SWOT)

TRANSCRIPT_DATA = {

    # ── Bajaj Finance ─────────────────────────────────────────────────────────
    # Source: Investor Call Transcript, April 29, 2026
    "Bajaj Finance": {
        "call_date": "April 29, 2026",
        "management": "Rajeev Jain (MD & CEO), Anup Saha (Deputy MD), Sandeep Jain (CFO)",
        "metric_comments": {
            "aum_cr": (
                "AUM crossed ₹5 lakh crore this quarter — 25% YoY growth. EMI finance, co-branded cards, "
                "and rural business lines all contributed. Management is targeting 25–27% AUM CAGR for FY27."
            ),
            "roa_pct": (
                "ROA stable at 4.65%. Management maintained 4.5–4.7% ROA guidance for FY27, reflecting "
                "structural profitability from the cross-sell engine and diversified product mix."
            ),
            "gnpa_pct": (
                "GNPA improved 20 bps QoQ to 1.01%. Underwriting was tightened in personal loans and EMI "
                "cards during H2 FY25; the benefit is now showing in slippage trends. No systemic stress flagged."
            ),
            "nim_pct": (
                "NIM ~10% range — stable. Rate-cut cycle expected to ease cost of funds; asset repricing is "
                "gradual, so NIM to remain range-bound in H1 FY27 before expanding in H2."
            ),
            "cost_of_borrowing_pct": (
                "Management flagged a metric change: credit cost reporting shifted to net-of-recoveries basis. "
                "Old metric: 165 bps gross. FY27 guidance: 145–160 bps net. CoB expected to ease as rate cuts "
                "transmit through the funding book."
            ),
            "car_pct": (
                "CAR well-maintained; no near-term equity raise indicated. Management believes current capital "
                "position supports 25–27% AUM growth for FY27 without dilution."
            ),
        },
        "guidance": [
            "AUM growth: 25–27% for FY27",
            "Credit cost (net of recoveries): 145–160 bps for FY27",
            "ROA: 4.5–4.7% maintained",
            "New loans: ~14 million per quarter run-rate",
            "NIM: stable at 10–10.5%; expansion expected in H2 FY27 as rate cuts transmit",
        ],
        "swot_prepend": {
            "S": [
                "GNPA 1.01% — underwriting tightened in H2 FY25 now reflecting in slippage trends; "
                "best-in-class asset quality in diversified retail",
                "ROA 4.65% — structurally highest in peer group; cross-sell engine driving 14 million "
                "new loans per quarter",
            ],
            "W": [
                "Credit cost metric shift (gross → net basis) reduces like-for-like comparability; "
                "one-off analytical complexity for the first 2 quarters",
                "NIM slightly softer as rate-cut expectations build; liability repricing slower than asset side",
            ],
            "O": [
                "Rate-cut cycle: cost of borrowing to ease; NIM expansion potential in H2 FY27",
                "Rural and Bharat expansion — low penetration, high growth adjacent to core urban business",
            ],
            "T": [
                "Regulatory scrutiny on FLDG structures and co-lending arrangements increasing",
                "Macro slowdown in consumer spending affecting EMI card and personal loan origination volumes",
            ],
        },
    },

    # ── L&T Finance ───────────────────────────────────────────────────────────
    # Source: Q4FY26 Earnings Call Transcript, April 27, 2026
    "L&T Finance": {
        "call_date": "April 27, 2026",
        "management": "Sudipta Roy (MD & CEO), Sachinn Joshi (CFO)",
        "metric_comments": {
            "aum_cr": (
                "AUM ₹1,21,728 Cr — 25% YoY. Retail mix now 97% of book. On track toward Lakshya 2026 "
                "target of ₹2 lakh crore AUM by FY28. Two-wheeler, farm, personal and home loans all growing."
            ),
            "roa_pct": (
                "ROA 2.40% (+3 bps QoQ). Management guided trajectory to 2.5–3% by FY28 as retail mix "
                "matures, credit costs normalize post ECL-model refresh, and operating leverage kicks in."
            ),
            "gnpa_pct": (
                "GNPA improved 31 bps QoQ to 2.88%. ECL model refresh completed — Stage 1 provision rate "
                "raised to 80 bps permanently, requiring a one-time ₹700 Cr charge in Q4. Management: "
                "'The book is now conservatively provisioned and we don't expect another reset.'"
            ),
            "nim_pct": (
                "NIMs stable. Rural and LAP portfolio yields holding up despite competitive pressure. "
                "Rate-cut cycle beneficial for cost of borrowing — NIM expansion expected as CoB eases "
                "faster than asset yields compress."
            ),
            "cost_of_borrowing_pct": (
                "CoB easing as L&T Finance's credit profile strengthens with retail mix. Rate-cut cycle "
                "adds a tailwind. Management expects NIM to expand as funding cost falls faster than "
                "asset yields in FY27."
            ),
            "car_pct": (
                "CAR comfortable; no equity raise needed for FY27 growth plan. Tier 1 well above "
                "regulatory minimum. Capital allocation supports 25%+ AUM growth without dilution."
            ),
        },
        "guidance": [
            "AUM growth: 25%+ for FY27; Lakshya 2026 target ₹2 lakh crore by FY28",
            "Credit cost: 200–250 bps for FY27 (front-loaded; ECL model refresh one-off — underlying stable)",
            "ROA: trajectory to 2.5–3% medium term (FY28 horizon)",
            "Stage 1 provision permanently at 80 bps — conservative ECL framework locked in",
            "Retail book mix target: 98%+ by FY27 end",
        ],
        "swot_prepend": {
            "S": [
                "GNPA improved 31 bps QoQ — ECL model refresh complete; Stage 1 provisioning raised to "
                "80 bps permanently; book conservatively positioned for future cycles",
                "AUM +25% YoY at ₹1.22 lakh crore — on track for Lakshya 2026 ₹2 lakh crore target by FY28",
            ],
            "W": [
                "ECL model refresh one-time ₹700 Cr charge in Q4; credit cost guidance of 200–250 bps "
                "for FY27 is elevated and weighs on near-term ROA",
                "ROA 2.40% still below management's own 2.5–3% medium-term target — execution risk on timeline",
            ],
            "O": [
                "Rate-cut cycle: CoB easing faster than asset yield compression — NIM expansion potential in FY27",
                "Retail mix now 97% — wholesale transition complete; credit cost to normalize as book seasons",
            ],
            "T": [
                "Front-loaded credit cost (200–250 bps) may disappoint if ECL refresh impacts persist beyond Q1 FY27",
                "Rural and LAP segments face competitive pricing pressure from banks entering these niches",
            ],
        },
    },

    # ── Aditya Birla Capital ──────────────────────────────────────────────────
    # Source: Q4FY26 Earnings Call Transcript, May 4, 2026
    "Aditya Birla Capital": {
        "call_date": "May 4, 2026",
        "management": "Vishakha Mulye (CEO), Rakesh Singh (CEO – ABFL), Pankaj Gadgil (CEO – ABHFL)",
        "metric_comments": {
            "aum_cr": (
                "NBFC AUM ₹1,26,351 Cr + HFC ₹31,053 Cr = ₹1,57,404 Cr total (+25% YoY). Growth broad-based "
                "across mortgage, SME, and personal finance. Co-lending partnerships expanding off-balance-sheet AUM."
            ),
            "roa_pct": (
                "NBFC-only ROA 2.31% (+6 bps QoQ). Consolidated ROA diluted by HFC book (structurally lower). "
                "Management's focus: scale secured retail mix to improve consolidated ROA toward NBFC-level returns."
            ),
            "gnpa_pct": (
                "GNPA 1.33% (-18 bps QoQ). Management: retail collections remain strong; corporate stress largely "
                "behind us. Co-lending partnerships keeping origination quality high. Target below 1.2% by FY27."
            ),
            "nim_pct": (
                "NIM stable. Co-lending arrangements reduce on-balance-sheet CoB; off-balance-sheet income "
                "contribution growing. Net effect: NIM holds steady while capital efficiency improves."
            ),
            "cost_of_borrowing_pct": (
                "CoB moderating as ABCL's credit profile strengthens with scale and retail mix improvement. "
                "Increasing co-lending partnerships optimize funding cost on partnered book segments."
            ),
            "car_pct": (
                "CAR comfortable across entities. Group has adequate capital for 25%+ AUM growth in FY27 "
                "without equity raise. HFC Tier 1 above NHB regulatory minimum."
            ),
        },
        "guidance": [
            "AUM growth: 25%+ for FY27 across NBFC + HFC combined",
            "GNPA: target below 1.2% by FY27",
            "ROA: improvement trajectory as retail secured mix scales up",
            "Co-lending book to grow as ABCL deepens bank partnerships",
            "HFC book: scaling mortgage penetration as a long-runway structural play",
        ],
        "swot_prepend": {
            "S": [
                "GNPA 1.33% and declining — retail collections robust; corporate stress resolved; "
                "best credit quality for a diversified NBFC+HFC book of this size",
                "25% YoY AUM growth — broad-based across mortgage, SME, and personal finance; "
                "co-lending adding asset-light scale",
            ],
            "W": [
                "Consolidated ROA diluted by HFC book (lower ROA than NBFC); NBFC-only 2.31% not directly "
                "comparable to peers reporting on purely NBFC consolidated basis",
                "Brand and distribution reach still narrower than Bajaj or Shriram in semi-urban geographies",
            ],
            "O": [
                "Co-lending partnerships expanding — reduce CoB on partnered book while growing AUM asset-light",
                "HFC book scaling — mortgage penetration in India structurally under-served; long growth runway",
            ],
            "T": [
                "HFC segment faces housing slowdown risk if rate cuts don't transmit to home buyer affordability",
                "Co-lending model subject to evolving FLDG regulation — guideline changes could impact economics",
            ],
        },
    },

    # ── Mahindra Finance ──────────────────────────────────────────────────────
    # Source: Q4FY26 Earnings Call Transcript, April 24, 2026
    "Mahindra Finance": {
        "call_date": "April 24, 2026",
        "management": "Raul Rebello (MD & CEO), Pradeep Agrawal (CFO), Sandeep Mandrekar (CBO Wheels)",
        "metric_comments": {
            "aum_cr": (
                "Business AUM +12% FY26. Tractor disbursements +63% in Q4 — Mahindra Finance is #1 in tractor "
                "financing. SME book +32%; cross-sell PPC at 2.4 (from under 2 a year ago). Management guided "
                "mid-teen AUM growth for FY27."
            ),
            "roa_pct": (
                "Q4 ROA 2.4% (2.9% ex-overlay). Management created ₹217 Cr management overlay for West Asia "
                "war and monsoon risk — macro-prudential, not linked to actual collection performance. April "
                "collections showed no impact. Overlay will be released if headwinds don't materialize."
            ),
            "gnpa_pct": (
                "GS3 3.4% (-39 bps QoQ) — record low since 2016. GS2+GS3 8.18% — 8-year low. Management: "
                "'This is the best asset quality in the company's history.' PCR 58.6%."
            ),
            "nim_pct": (
                "NIM +101 bps YoY in Q4. Management views 7.1% NIM as more sustainable than the prior 7.5% "
                "target. Fee income reached 1.4% of assets (up from 1.1%) — structural growth target 1.5–1.6% "
                "medium term."
            ),
            "cost_of_borrowing_pct": (
                "₹35,000–40,000 Cr borrowings maturing in FY27 — to be refinanced at lower rates as rate "
                "cut cycle progresses. Management flagged this as a significant CoB tailwind for FY27."
            ),
            "car_pct": (
                "CAR 18.8%, Tier 1 16.7%. Capital adequate for mid-teen AUM growth. Board to decide on "
                "mortgage structure (HFC vs NBFC license) by Q2 FY27."
            ),
        },
        "guidance": [
            "AUM growth: mid-teen for FY27",
            "Credit cost: 1.3–1.7% (normalized business-model range for FY27)",
            "ROE aspiration: 15% medium-term; currently 12.5%",
            "ROE target requires D/E ~6:1 + ROA 2.0–2.2%",
            "₹35,000–40,000 Cr borrowings maturing FY27 — refinancing at lower rates expected",
            "Mortgage structure (HFC vs NBFC license): Board decision by Q2 FY27",
            "50% of FY26 disbursements on Udaan digital platform; further improvement targeted",
        ],
        "swot_prepend": {
            "S": [
                "GS3 3.4% — record low since 2016; GS2+GS3 8.18% — 8-year low; collection engine "
                "at historic best performance",
                "Tractor financing #1 market position; disbursements +63% Q4; structural rural vehicle moat",
            ],
            "W": [
                "₹217 Cr management overlay reduces reported Q4 PAT — macro-prudential buffer not linked "
                "to actual collections; but adds uncertainty for investors reading headline numbers",
                "ROE 12.5% — below 15% aspiration; requires D/E ~6x + ROA 2–2.2%; capital structure work needed",
            ],
            "O": [
                "₹35,000–40,000 Cr borrowings maturing FY27 — refinancing at lower rates; material CoB tailwind",
                "SME book +32% and cross-sell PPC at 2.4 — significant under-penetration vs 24 lakh live customers",
            ],
            "T": [
                "West Asia war impact on remittance-dependent states (Kerala) — monitoring; no April impact yet; "
                "Q2 FY27 is the watch window for 90-day delinquency metric",
                "Monsoon dependency of rural portfolio — tractor and agri-linked segments sensitive to rainfall",
            ],
        },
    },

    # ── Piramal Finance ───────────────────────────────────────────────────────
    # Source: Q4FY26 Earnings Call Transcript, April 27, 2026
    "Piramal Finance": {
        "call_date": "April 27, 2026",
        "management": "Anand Piramal (Executive Chairman), Jairam Sridharan (MD & CEO), Rupen Jhaveri (Group President), Vikash Singhla (CFO)",
        "metric_comments": {
            "aum_cr": (
                "AUM crossed ₹1 lakh crore milestone — ₹1,01,230 Cr (+25% YoY). Retail 85% of total. "
                "Wholesale 2.0 book ₹12,538 Cr with zero NPAs. Legacy book <3% of AUM (-59% YoY) — "
                "will become irrelevant by H2 FY27."
            ),
            "roa_pct": (
                "Growth book ROaAUM 2.1% Q4 (vs 1.7% Q4FY25). Management guided exit FY27 ROaAUM of 2.5% "
                "via: ~50 bps opex leverage (ops staff flat while AUM doubled) + 50–80 bps CoF reduction "
                "from AA+ rating upgrade."
            ),
            "gnpa_pct": (
                "GNPA 2.3% (-30 bps QoQ). NNPA 1.6% (-30 bps QoQ). Micro-loan portfolio 'almost completely "
                "normalized'. 90+ delinquencies at 0.6% (-20 bps QoQ). AI used to rapidly scan industry "
                "sub-segments by Iran-war sensitivity."
            ),
            "nim_pct": (
                "Growth book NIM 7%. Consolidated NIM 6.5% (+20 bps QoQ). Opex/AUM 3.6% (-21 bps QoQ) — "
                "cost discipline allowing NIM gains to flow to bottom line. AI token volume: 178 billion "
                "in Q4 vs 63 billion in Q1 FY26."
            ),
            "cost_of_borrowing_pct": (
                "CoB 8.84% (-11 bps QoQ). AA+ rating upgrade from all 3 agencies — management expects "
                "50–80 bps cost of funds savings over 3 years as book churns. Incremental LT debt already "
                "at 8.4%; short-term at ~7.25%. LCR 450% average Q4."
            ),
            "car_pct": (
                "CAR 19.8%; leverage 3.6x (target 4.5–5x). ₹24,600 Cr accumulated tax losses shield profits "
                "until ~2032 (PBT ≈ PAT effectively). Net capital consumption: 50 bps/quarter at current "
                "growth pace."
            ),
        },
        "guidance": [
            "AUM growth: +25% for FY27",
            "Consolidated profits: +50% for FY27 (FY26: ₹1,506 Cr → FY27 target ~₹2,259 Cr)",
            "Exit FY27 ROaAUM: 2.5% (growth book) via opex leverage + CoF reduction",
            "Cost of funds: 50–80 bps savings over 3 years post AA+ upgrade",
            "Legacy book: irrelevant by H2 FY27; segment reporting to be discontinued",
            "Gold loan expansion: ~200 branches by end FY27 (Phase 1 — Maharashtra & Telangana)",
            "Tax shield: ₹24,600 Cr accumulated losses → PBT ≈ PAT until ~2032",
        ],
        "swot_prepend": {
            "S": [
                "AA+ rating upgrade from all 3 agencies — 50–80 bps CoF savings expected over 3 years; "
                "structural funding cost advantage now locked in",
                "₹24,600 Cr accumulated tax losses → PBT ≈ PAT until ~2032; tax shield materially "
                "boosts net profitability vs peers",
            ],
            "W": [
                "Leverage 3.6x vs target 4.5–5x — underlevered; needs capital deployment acceleration "
                "to optimize ROE from current levels",
                "Legacy book still 3% of AUM — drag on consolidated GNPA and credit cost until H2 FY27 "
                "wind-down completes",
            ],
            "O": [
                "AA+ upgrade → 50–80 bps CoF reduction over 3 years as book churns → direct NIM/ROA uplift",
                "AI operating leverage — token volume 178B in Q4 vs 63B in Q1 FY26; ops staff flat while "
                "AUM doubled; path to 2.5% ROaAUM confirmed via opex efficiency",
            ],
            "T": [
                "West Asia war: micro-loan exposure in remittance-dependent geographies; "
                "Q2 FY27 is key watch window for 90-day delinquency metric",
                "Gold loan entry (Phase 1) carries execution risk — regulatory, geographic, and competitive "
                "headwinds in an established market dominated by Muthoot and Manappuram",
            ],
        },
    },

    # ── Shriram Finance ───────────────────────────────────────────────────────
    # Source: Q4FY26 earnings call transcript via Morningstar, April 2026
    "Shriram Finance": {
        "call_date": "April 2026 (Q4FY26 earnings call)",
        "management": "Y. S. Chakravarti (MD & CEO), Parag Sharma (Joint MD & CFO)",
        "metric_comments": {
            "aum_cr": (
                "AUM ₹3,02,274 Cr (+15% YoY). Commercial vehicle segment remains the core — #1 CV lender "
                "in India. Management focused on maintaining CV/MSME dominance while growing SME and used-asset "
                "sub-segments."
            ),
            "roa_pct": (
                "ROA 3.63% — structurally among the highest in the commercial vehicle NBFC segment. "
                "Reflects strong asset yields in used CV and MSME lending, and an efficient "
                "pan-India collection infrastructure built over decades."
            ),
            "gnpa_pct": (
                "GNPA 4.58% — elevated vs consumer finance peers, but normalized for the commercial vehicle "
                "and self-employed MSME segment. Management highlighted stable collection efficiency "
                "and improving freight cycle as tailwinds for FY27."
            ),
            "car_pct": (
                "CAR 20.40% — well above RBI 15% floor. D/E 3.8x — conservative leverage provides "
                "significant room to accelerate book growth in FY27 without capital raise."
            ),
        },
        "guidance": [
            "AUM growth: 15%+ for FY27; CV sector recovery supporting disbursement volumes",
            "Credit cost: within segment norms; GNPA expected to moderate as CV freight cycle improves",
            "ROA: 3.2–3.6% structural range; supported by used-CV yield premium",
            "Capital deployment: D/E headroom to grow book more aggressively if CV demand recovers",
        ],
        "swot_prepend": {
            "S": [
                "ROA 3.63% — structural advantage from used-CV and MSME yield premium; #1 CV lender "
                "franchise with pan-India collection infrastructure",
                "CAR 20.40% and D/E 3.8x — conservatively capitalized; ample headroom to accelerate "
                "book growth without equity raise",
            ],
            "W": [
                "GNPA 4.58% — structural floor due to self-employed borrower base with lumpy repayment "
                "profile; hard to bring below 4% without changing borrower mix",
                "NNPA 2.33% — net credit risk highest in peer group; PCR needs to remain robust to "
                "maintain balance sheet strength",
            ],
            "O": [
                "CV freight cycle recovery — improved road freight volumes and fleet operator profitability "
                "directly reduce slippages and support new disbursements",
                "SME and micro-enterprise cross-sell to existing CV customer base — natural adjacency",
            ],
            "T": [
                "GNPA at 4.58% — any macro slowdown in freight or construction sector could push NPA higher; "
                "Watch West Asia conflict impact on trucking demand",
                "Competition from banks entering used CV financing with lower cost of funds — yield compression risk",
            ],
        },
    },

    # ── Poonawalla Fincorp ────────────────────────────────────────────────────
    # Source: Q4FY26 earnings call transcript, April 2026
    "Poonawalla Fincorp": {
        "call_date": "April 2026 (Q4FY26 earnings call)",
        "management": "Arvind Kapil (MD & CEO)",
        "metric_comments": {
            "aum_cr": (
                "AUM ₹60,348 Cr (+9.7% QoQ). Strong recovery trajectory from FY25 disruption. Consumer and "
                "personal finance focus on salaried and self-employed segments. Book quality preserved through "
                "selective underwriting even during the provision-heavy FY25 phase."
            ),
            "roa_pct": (
                "ROA 1.81% (+61 bps QoQ) — sharp sequential recovery as the one-time ₹666 Cr FY25 provision "
                "washes out. Management indicated trajectory back toward 2%+ as the book seasons and "
                "provisions normalize."
            ),
            "gnpa_pct": (
                "GNPA 1.44% — among the lowest in the peer group. Selective underwriting in the salaried "
                "segment is the structural driver of best-in-class asset quality. Management has no intent "
                "to compromise on quality for volume."
            ),
            "pat_cr": (
                "PAT ₹255 Cr (+70% QoQ). Recovery firmly on track. FY25 one-time provision (₹666 Cr) "
                "does not recur; next 4 quarters set up for clean PAT growth. Full FY26 PAT ₹542 Cr "
                "partially reflects the FY25 overhang."
            ),
        },
        "guidance": [
            "ROA recovery trajectory: target 2%+ as FY25 provision impact fully washes out",
            "AUM: strong growth momentum to continue (smaller base = higher CAGR potential)",
            "GNPA: target sub-1.5%; quality-first underwriting maintained",
            "Book mix: consumer + personal finance anchored in salaried segment",
            "No recurrence of FY25-style one-time provisions; clean earnings from FY26 onward",
        ],
        "swot_prepend": {
            "S": [
                "GNPA 1.44% — best-in-class; selective salaried-segment underwriting creates structural "
                "asset quality moat vs vehicle and CV peers",
                "ROA +61 bps QoQ — sharp rebound as FY25 one-time provision (₹666 Cr) does not recur; "
                "clean earnings trajectory from FY26 onward",
            ],
            "W": [
                "Smallest AUM (₹60k Cr) in peer group — scale limitations in funding cost, bargaining power, "
                "and fixed-cost absorption vs Bajaj (₹510k Cr) or Shriram (₹302k Cr)",
                "ROA 1.81% still rebuilding from FY25 provision hit; PAT ₹255 Cr modest in absolute terms",
            ],
            "O": [
                "FY25 provision clean-up complete — clean balance sheet; next 4 quarters set up for strong "
                "PAT growth without one-time drag",
                "Consumer finance penetration deepening; rising salaried workforce in India supports TAM growth",
            ],
            "T": [
                "Competition in personal loans intensifying from banks and fintechs — yield pressure on core product",
                "Regulatory risk: RBI focus on unsecured lending could tighten eligibility or require higher provisions",
            ],
        },
    },

    # ── Cholamandalam Finance ─────────────────────────────────────────────────
    # Source: Q4FY26 earnings call transcript, April/May 2026
    "Chola Finance": {
        "call_date": "April/May 2026 (Q4FY26 earnings call)",
        "management": "Vellayan Subbiah (MD), Arul Selvan (CFO)",
        "metric_comments": {
            "aum_cr": (
                "AUM ₹2,42,630 Cr (+14.9k QoQ). Vehicle finance remains core; home loans and SME lending "
                "growing at above-portfolio pace. Broad-based disbursement recovery driven by rural income "
                "improvement and fleet operator demand."
            ),
            "roa_pct": (
                "ROA 2.90% (-30 bps QoQ) — slight moderation from peak. Margin pressure from competitive "
                "vehicle finance pricing. Management views 2.8–3.0% as the sustainable ROA band for "
                "the current product mix."
            ),
            "gnpa_pct": (
                "GNPA 4.36% (-27 bps QoQ). NNPA 2.87% (-26 bps QoQ). Steady sequential improvement — "
                "vehicle segment collection efficiency recovering with rural income improvement and "
                "better monsoon outcomes."
            ),
            "nim_pct": (
                "NIM stable. Vehicle finance yields holding; home loan yields slightly compressed by "
                "competition. SME book expansion supporting yield mix and partially offsetting "
                "vehicle pricing pressure."
            ),
        },
        "guidance": [
            "AUM growth: 20%+ for FY27; vehicle, home, and SME all contributing",
            "GNPA: continued improvement trajectory toward 4% range",
            "ROA: stabilize at 2.8–3.0%; NIM protected through product mix",
            "SME and home loan growth at above-portfolio rates to improve margin mix",
        ],
        "swot_prepend": {
            "S": [
                "GNPA -27 bps QoQ and NNPA -26 bps QoQ — sequential credit quality improvement driven by "
                "rural collection recovery; trend consistent for 3 quarters",
                "PAT +27.4% QoQ — strong sequential earnings momentum; diversified vehicle + home + SME "
                "product mix proving resilient",
            ],
            "W": [
                "GNPA 4.36% — elevated vs peer median; vehicle and rural portfolio has structural NPA floor "
                "given self-employed borrower mix; hard to sustain below 4%",
                "ROA -30 bps QoQ — margin compression from competitive vehicle finance pricing; "
                "2.90% vs sector norms still acceptable but directionally concerning",
            ],
            "O": [
                "Rural income improvement and good monsoon → direct tailwind for vehicle portfolio repayment "
                "and new disbursements; tractor and agri-linked demand benefits Chola",
                "Home loan and SME books growing faster than vehicle — margin-accretive mix shift underway",
            ],
            "T": [
                "GNPA 4.36% still elevated — any rural stress (drought, commodity collapse) could reverse "
                "the improvement trend sharply",
                "Competitive intensity in new vehicle finance from OEM captive NBFCs and banks with lower CoB",
            ],
        },
    },

    # ── Muthoot Finance ───────────────────────────────────────────────────────
    # Source: Q4FY26 Investor Presentation (May 14, 2026); standalone basis
    # Note: Muthoot earnings call transcript not separately ingested;
    #       data from investor deck + disclosed metrics
    "Muthoot Finance": {
        "call_date": "May 14, 2026 (Q4FY26 investor presentation)",
        "management": "George Alexander Muthoot (MD), George M. George (Exec Director), George Thomas Muthoot (Exec Director)",
        "metric_comments": {
            "aum_cr": (
                "Standalone AUM ₹1,62,826 Cr (+50% YoY) — gold price appreciation and branch expansion "
                "driving extraordinary growth. Gold AUM per branch increasing alongside network expansion. "
                "Standalone basis; consolidated includes subsidiaries (Belstar Microfinance, Lanka)."
            ),
            "roa_pct": (
                "ROA 7.55% FY26 (PAT/Avg Loan Assets — Muthoot-disclosed metric). Structurally 4–7% for "
                "gold loans — not comparable to consumer/vehicle finance peers whose ROA is on total assets. "
                "FY26 uplift driven by record PAT ₹10,134 Cr and gold price gains."
            ),
            "gnpa_pct": (
                "GNPA not directly disclosed for gold loans (loan-to-value and auction mechanism is the "
                "primary risk control; NPA structure differs from conventional lending). Gold collateral "
                "provides near-complete loss protection."
            ),
            "car_pct": (
                "CAR well-above regulatory minimum. Gold loan business is capital-light relative to credit "
                "risk — collateral coverage provides effective capital protection. "
                "Muthoot operates with conservative LTV ratios per RBI guidelines."
            ),
        },
        "guidance": [
            "AUM growth: continued strong momentum driven by gold price appreciation and branch expansion",
            "PAT: FY26 ₹10,134 Cr (+95% YoY) — exceptional; gold price gains a key driver",
            "ROA: 6–8% structurally sustainable; FY26 7.55% reflects elevated gold price environment",
            "Branch network expansion: continued India + subsidiaries (Lanka, Belstar)",
            "Note: ROA not comparable to peer group — gold collateral structure is fundamentally different",
        ],
        "swot_prepend": {
            "S": [
                "ROA 7.55% — structurally highest in peer group; gold collateral model provides near-zero "
                "credit loss with high-yield asset; PAT ₹10,134 Cr FY26 (+95% YoY)",
                "AUM +50% YoY — extraordinary growth from gold price appreciation + branch expansion; "
                "no credit underwriting risk in conventional sense",
            ],
            "W": [
                "ROA not comparable to peers — gold loan structure (PAT/Loan Assets vs PAT/Total Assets) "
                "inflates the metric vs conventional NBFCs",
                "Gold price dependency — AUM and PAT meaningfully sensitive to gold price cycles; "
                "a sharp gold price correction would reduce AUM and LTV headroom",
            ],
            "O": [
                "Gold price staying elevated globally — continued AUM and NIM tailwind in FY27",
                "Belstar Microfinance (subsidiary) normalizing — reduction in microfinance stress improves "
                "consolidated profitability",
            ],
            "T": [
                "RBI regulation on gold loan LTV and auction practices — any tightening could reduce "
                "eligible AUM or increase operational complexity",
                "Competition intensifying: Piramal Finance entering gold loans, banks expanding gold loan products",
            ],
        },
    },
}
