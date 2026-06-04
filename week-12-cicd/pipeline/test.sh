#!/bin/bash
set -e

echo "=== STAGE: TEST ==="
echo "Running unit tests..."

python3 app/tests/test_app.py -v

echo ""
echo "✓ All tests passed"
