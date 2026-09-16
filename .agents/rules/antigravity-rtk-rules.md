# RTK - Rust Token Killer (Google Antigravity)

**Usage**: Token-optimized CLI proxy for terminal commands executed via `run_command`.

## Core Guidelines

1. **Test Runners, Linters & Git**:
   Prefix terminal commands with `rtk` when running test suites, linters, builds, and git inspections via `run_command`:
   ```bash
   rtk pytest
   rtk vitest
   rtk cargo test
   rtk ruff check .
   rtk tsc --noEmit
   rtk git status
   rtk git diff
   rtk docker ps
   rtk gh pr list
   ```

2. **Native Tool Boundary (CRITICAL)**:
   * **Do NOT** use `rtk read`, `rtk grep`, `rtk find`, or `rtk ls` via bash/`run_command`.
   * **Always prioritize Antigravity's native tools** (`view_file`, `grep_search`, `find_by_name`, `list_dir`). Native tools are token-bounded, support precise line slicing, and integrate with Antigravity's IDE diffing.

3. **Debugging Fallback**:
   If a test or build fails mysteriously and detailed error output is truncated, run the raw command without `rtk` (or use `rtk proxy <cmd>`) to inspect complete diagnostic output.

## Meta Commands
```bash
rtk gain              # Show token savings
rtk discover          # Find missed RTK opportunities
rtk proxy <cmd>       # Run raw (no filtering, for debugging)
```
