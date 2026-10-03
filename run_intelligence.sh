#!/bin/bash

export PATH="/opt/homebrew/bin:$PATH"

cd /Users/ighokarl/shell-monitor

/Users/ighokarl/shell-monitor/.venv/bin/python multi_account_intelligence.py >> intelligence.log 2>&1