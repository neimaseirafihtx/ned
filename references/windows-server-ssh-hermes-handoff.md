# SSH & Hermes Setup Handoff — Windows Server (`NEIMA_SERVER`)

_Last updated: 2026-06-07_

We got SSH working from the MBP to the Windows machine and fixed Hermes. This is the current state.

## SSH is fully configured

- MBP connects via `ssh neima-server` (alias in `~/.zshrc`) → `192.168.68.89`
- Tailscale alias `neima-server-remote` → `100.120.157.4` for off-network access
- Key-based auth uses `~/.ssh/id_ed25519`; no password needed
- SSH config lives at `/Users/neima/.ssh/config` on the MBP

## Hermes over SSH is fixed

Hermes on Windows was broken over SSH due to a `uv` trampoline issue.

### Root cause

`uv`'s managed Python at:

```text
C:\Users\neima\AppData\Roaming\uv\python\cpython-3.11-windows-x86_64-none\
```

was blocked by Windows security in SSH sessions with:

```text
os error 448 - untrusted mount point
```

### Fix applied

Edited:

```text
C:\Users\neima\bin\hermes.cmd
```

to point `HERMES_PYTHON` to system Python 3.13:

```text
C:\Users\neima\AppData\Local\Programs\Python\Python313\python.exe
```

instead of the venv Python.

Then installed `hermes-agent` dependencies into system Python from:

```text
C:\Users\neima\AppData\Local\hermes\hermes-agent
```

with:

```powershell
pip install -e .
```

Hermes is now fully functional over SSH.

## Watch out

If Hermes auto-updates and rewrites `hermes.cmd`, it may revert `HERMES_PYTHON` back to the venv path and break again over SSH.

If that happens, re-run this on the Windows machine:

```powershell
powershell -Command "(Get-Content C:\Users\neima\bin\hermes.cmd) -replace 'C:\\Users\\neima\\AppData\\Local\\hermes\\hermes-agent\\venv\\Scripts\\python.exe', 'C:\\Users\\neima\\AppData\\Local\\Programs\\Python\\Python313\\python.exe' | Set-Content C:\Users\neima\bin\hermes.cmd"
```

## Next possible work

- Set up additional Windows server services.
- Continue home-lab migration work.
- Harden the Hermes Windows launcher so auto-updates do not silently undo the SSH-safe Python path.
