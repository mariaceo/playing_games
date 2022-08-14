# install Playwright
```playwright install```

## run tests
```pytest test/test_checkers.py --headed --slowmo 100```

## run tests with tracing
```pytest --headed --tracing retain-on-failure```

# show the trace
```playwright show-trace test-results/test-checker-py-test-checkers-chromium/trace.zip```