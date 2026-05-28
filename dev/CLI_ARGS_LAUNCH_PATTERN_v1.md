# HS-051 — ⌨️ CLI COMMANDER — CLI Args Launch Pattern

> *"Flags first. No flag = safe default. Every option is explicit and documented."*

---

## 🎯 What It Does
The standard CLI argument pattern used across HyperFocus scripts. Argparse-based, with safe defaults, explicit flags, and built-in help text.

## 🌍 Why It Exists
Inconsistent CLI interfaces across scripts create confusion. This pattern makes every HyperFocus script feel like the same tool.

## ⚙️ How To Use
1. Use as the base template for any new Python CLI script
2. Add your flags following the pattern below
3. Always include `--dry-run` for destructive operations

---

## 📋 THE PROMPT

```
Create CLI args for script: [SCRIPT_NAME]
Purpose: [SCRIPT_PURPOSE]

```python
import argparse

def parse_args():
    parser = argparse.ArgumentParser(
        description='[SCRIPT_PURPOSE]',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    # Core flags
    parser.add_argument('--profile', choices=['core', 'discord', 'full', 'nemoclaw'],
                        default='core', help='Docker compose profile to use (default: core)')
    parser.add_argument('--verify', action='store_true',
                        help='Run health verification after launch')
    parser.add_argument('--dry-run', action='store_true',
                        help='Print what would happen without doing it')
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='Verbose output')

    # Custom flags for [SCRIPT_NAME]
    # parser.add_argument('--[FLAG]', ...)

    return parser.parse_args()

def main():
    args = parse_args()

    if args.dry_run:
        print("[DRY RUN] Would execute: [SCRIPT_PURPOSE]")
        return

    if args.verbose:
        print(f"Profile: {args.profile}")
        print(f"Verify: {args.verify}")

    # Your script logic here
    run(profile=args.profile, verify=args.verify)

if __name__ == '__main__':
    main()
```

HyperFocus CLI conventions:
- Default = safest option
- --dry-run on ALL destructive ops
- --verbose for debug output
- --profile for environment selection
- Always print what you're about to do before doing it
```

---

## 🔗 Related Skills
- HS-046 — LAUNCH SOVEREIGN
- HS-048 — PREFLIGHT ACE
- HS-039 — CLOSE PROTOCOL

---
*HYPER-SKILLs Vault — welshDog 🐕🏴󠁧󠁢󠁷󠁬󠁳󠁧⚡*