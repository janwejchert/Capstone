"""Top-level simulation loop.

Runs T periods following the intra-period timing fixed in section 3.6 of the
proposal:

    1. Agents form forecasts using returns up to and including period t.
    2. Adopters and non-adopters submit orders.
    3. The market maker absorbs aggregate demand and moves the quote.
    4. The exogenous news shock and residual AR term realise.

Phase 1 adds the loop with null traders only. Later phases add the forecast,
adoption, and switching steps.
"""
