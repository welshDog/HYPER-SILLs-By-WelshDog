# HS-051 — ⌨️ CLI ARGS LAUNCH — CLI Args Launch Pattern

## What it Does
Standard CLI argument pattern for V2.4 launch scripts. Enables profile selection, tier targeting, dry-run mode, and verbose output from the command line.

## When To Use
- Building any launch or management script for V2.4
- Adding CLI controls to an existing Python script
- Designing operator-friendly tooling

## THE PATTERN
```python
import argparse
import sys

def parse_args():
    parser = argparse.ArgumentParser(
        description='🚀 HyperCode Launch Commander',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python hyperlaunch.py                          # Full stack launch
  python hyperlaunch.py --profile discord        # Include bot
  python hyperlaunch.py --tier 2                 # Core only (tiers 1-2)
  python hyperlaunch.py --dry-run                # Show plan, don’t launch
  python hyperlaunch.py --skip-preflight         # Skip env check (not recommended)
  python hyperlaunch.py --verbose                # Show all health check attempts
"""
    )

    parser.add_argument(
        '--profile', '-p',
        choices=['discord', 'brain', 'nemoclaw', 'full'],
        help='Docker compose profile to activate'
    )
    parser.add_argument(
        '--tier', '-t',
        type=int, choices=[1, 2, 3, 4], default=4,
        help='Launch up to this tier (default: all tiers)'
    )
    parser.add_argument(
        '--dry-run', action='store_true',
        help='Show launch plan without executing'
    )
    parser.add_argument(
        '--skip-preflight', action='store_true',
        help='Skip env preflight check (NOT recommended)'
    )
    parser.add_argument(
        '--verbose', '-v', action='store_true',
        help='Verbose health check output'
    )
    parser.add_argument(
        '--timeout', type=int, default=60,
        help='Health check timeout per service in seconds (default: 60)'
    )

    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()

    if not args.skip_preflight:
        run_preflight(args.profile)  # HS-048

    if args.dry_run:
        show_launch_plan(args.tier, args.profile)
        sys.exit(0)

    launch(tier_max=args.tier, profile=args.profile, verbose=args.verbose)
```

## Related Skills
- HS-046 HYPERLAUNCH UNIFIED COMMANDER
- HS-048 PREFLIGHT CHECKS System
- HS-064 Dev Commands Cheat Sheet

---
*Source: HyperCode-V2.4 hyperlaunch.py | Category: dev/*
