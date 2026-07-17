# Honesty Model

## Checks Included

### Chronology

- Signal timestamps must precede entries.
- Exit timestamps cannot precede entries.
- Feature timestamps may not occur after the signal timestamp.

### Position Overlap

The audit can reject overlapping positions in the same symbol. This models live systems that permit only one active position per symbol.

### Ambiguous OHLC Bars

When both stop and target are touched inside one OHLC bar, the intrabar path is unknown. The toolkit supports three explicit policies:

- `conservative`: assume the adverse level was reached first;
- `optimistic`: assume the favorable level was reached first;
- `reject`: exclude the ambiguous result from evidence.

### Costs

Transaction costs are applied as explicit round-trip commission and slippage amounts rather than being silently omitted.

### Equity Reconstruction

Closed trades are sorted chronologically before calculating equity, peaks, and drawdowns.

## Excluded by Design

- Strategy rules
- Signal thresholds
- Instrument-selection logic
- Position-sizing edge
- Broker credentials
- Live order submission
- Proprietary research results
