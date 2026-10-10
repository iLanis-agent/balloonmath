# Balloon math

Party balloon planning without the sad surprises. A static site with three calculators:

- **Tank fill** - helium liters become a balloon count and the leftover, at labeled fill volumes.
- **Arch count** - arch meters become clusters and balloons, at a labeled cluster spacing.
- **Float window** - hours until the event become inflate-now or wait, at labeled float estimates.

Live site: https://ilanis-agent.github.io/balloonmath/

## Labeled norms

Labeled party estimates - your tank gauge and your balloons win:

- Fill volumes: 23 cm balloon about 7 L, 28 cm about 14 L, 40 cm about 42 L.
- Arch: a 4-balloon cluster every 25 cm.
- Float time: latex about 10 h, foil about 120 h. Altitude and temperature shift it.

## Layout

- `engine.js` - pure arithmetic and text rendering, shared by the page and the tests.
- `index.html` - landing page. `app.html` - the calculators.
- `oracle.py` - independent Python mirror of the engine's exact float operations.
- `expected.json` - 36 oracle-generated cases. `test.js` - runs every case against the engine plus render checks.

## Tests

```
python3 oracle.py   # regenerate expected.json
node test.js        # 108 checks, 0 failures
```
