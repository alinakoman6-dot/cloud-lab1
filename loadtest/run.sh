#!/usr/bin/env bash
set -e
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
export BASE_URL="http://$(terraform -chdir=terraform output -raw alb_dns_name)"
VUS=${VUS:-30} k6 run loadtest/script.js