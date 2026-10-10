# Analytics audit and refactor priorities

Audit date: 10 October 2026. Sources were inspected read-only.

## Verified baseline

- Resort Hotel rows: **40,060**.
- Canceled: **11,122**; not canceled: **28,938**; overall cancellation rate: **27.76%**.
- Deck annual counts reconcile to the overall total:
  - 2015: 2,138 canceled / 8,314 bookings = **25.72%**.
  - 2016: 4,930 / 18,567 = **26.55%**.
  - 2017: 4,054 / 13,179 = **30.76%**.
- Customer-type results in the sheet: Transient 31.17%, Contract 8.84%, Group 10.56%, Transient-Party 19.50%.
- Distribution-channel results in the sheet: Direct 16.85%, Corporate 21.05%, TA/TO 31.49%.

## Confirmed defects and risks

1. **Repeated-guest chart uses the wrong field.** The `An.Repeat` formulas label rows as distribution channels but filter `data_atribut!E:E`, which is `market_segment`; the actual distribution channel is column H. This explains the impossible TA/TO value of zero and invalidates the chart and related recommendation until recalculated.
2. **The proposed 589-day cutoff is unsupported.** The 590-737 bucket contains only two bookings, both not canceled. A 0% rate from n=2 is not evidence that 589 days is an operational threshold. The adjacent 443-589 bucket contains 105 bookings and has a 54.29% cancellation rate.
3. **Bucket design is too coarse and uneven for a policy decision.** Equal-width lead-time buckets hide the practical concentration of bookings. Use business-relevant intervals (for example 0-7, 8-30, 31-90, 91-180, 181-365, >365), report n and confidence intervals, and test sensitivity.
4. **Recommendations imply causality from descriptive EDA.** The dataset can show association, not prove that discounts, loyalty treatment, or a lead-time limit will reduce cancellations by five percentage points. Reframe these as hypotheses for experiments.
5. **Repeated bookings are counts of bookings, not necessarily unique customers.** There is no stable customer identifier in the selected fields, so retention and loyalty claims must be qualified.
6. **Dashboard is currently accessible but not portfolio-ready.** On inspection, filters and multiple charts show system/data-source errors, including an unknown data source. The live dashboard cannot currently substantiate the deck.
7. **Documentation quality needs a pass.** Titles, field names, and narrative contain inconsistent spelling (`cancelation`, `costumer`, `leadtime`, `royalty` where `loyalty` is intended) and should use one metric definition throughout.

## Priority plan

### P0 - Correctness and reproducibility

- [x] Preserve original artifacts and record team attribution.
- [x] Reconcile the core cancellation totals and annual rates.
- [x] Identify the repeated-guest field mismatch and weak cutoff inference.
- [x] Add a reproducible calculation script and unit tests.
- [ ] Export a frozen raw-data snapshot with checksum and a data dictionary.
- [ ] Recalculate all charts from one cleaned table and document exclusions/null handling.

### P1 - Portfolio narrative

- [ ] Replace the 589-day recommendation with evidence-based segments and sample sizes.
- [ ] Separate findings, hypotheses, and proposed experiments.
- [ ] Repair or rebuild the Looker Studio data source and verify every chart against script output.
- [ ] Redesign the dashboard hierarchy: KPI definitions, trend, segment drivers, sample-size context, and limitations.
- [ ] Rewrite the deck in concise professional English or Indonesian, with sources and metric definitions.

### P2 - Stronger analysis

- [ ] Add uncertainty intervals and a simple multivariable cancellation model.
- [ ] Check leakage, class balance, seasonality, deposit type, booking changes, and market-segment interactions.
- [ ] Define an experiment: target segment, treatment, guardrails, minimum detectable effect, and evaluation window.
