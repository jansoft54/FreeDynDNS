#!/usr/bin/env bash

set -euo pipefail

if [[ $# -ne 2 ]]; then
  echo "Usage: $0 /path/to/freeDynDns.py /path/to/freeDynDns.log"
  exit 1
fi

SCRIPT_PATH="$1"
LOG_FILE="$2"
if [[ "${SCRIPT_PATH:0:1}" != "/" || "${LOG_FILE:0:1}" != "/" ]]; then
  echo "Please specify absolute paths for both the script and log file."
  exit 1
fi
PYTHON_BIN="$(command -v python3 || echo '/usr/bin/env python3')"

CRON_LINE_10="*/10 * * * * ${PYTHON_BIN} ${SCRIPT_PATH} >> ${LOG_FILE} 2>&1"
CRON_LINE_REBOOT="@reboot ${PYTHON_BIN} ${SCRIPT_PATH} >> ${LOG_FILE} 2>&1"

tmpfile="$(mktemp)"
trap 'rm -f "$tmpfile"' EXIT

crontab -l 2>/dev/null \
  | grep -vF "${SCRIPT_PATH}" \
  > "$tmpfile" || true

echo "$CRON_LINE_10"    >> "$tmpfile"
echo "$CRON_LINE_REBOOT" >> "$tmpfile"

crontab "$tmpfile"
# ─────────────────────────────────────────────────────────────────────────────

echo "✅ Installed cron jobs:"
echo "   every 10m:   $CRON_LINE_10"
echo "   at reboot:   $CRON_LINE_REBOOT"
