# Installing SubstrateOS

This guide takes you from nothing to running `subos claude` from any folder. It
is written for first-time users, no prior experience needed. Pick your operating
system below.

**What you get:** two commands on your PATH.

- **`subos`** launches an AI engine (Claude, Codex, Gemini, Cursor) as a
  SubstrateOS "kernel".
- **`labctl`** is the harness that runs the build discipline (status, ingest, the
  release gate, and more).

SubstrateOS does **not** include an AI model or any paid API. It launches whatever
engine you already have installed (e.g. the `claude` command), so there is no
extra billing from SubstrateOS itself.

---

## Before you start

You need two things:

1. **Python 3.11 or newer.** Check with `python --version` (or `python3 --version`).
   If it is missing or older, install it from <https://www.python.org/downloads/>.
   On Windows, tick **"Add python.exe to PATH"** in the installer.
2. **A copy of this repository.** Either download the ZIP from GitHub and unzip
   it, or, if you have `git`:

   ```sh
   git clone https://github.com/<owner>/SubstrateOS.git
   cd SubstrateOS
   ```

The installer lives at the top of the repository (`install.ps1` for Windows,
`install.sh` for Linux/macOS). Run it from inside the repository folder.

---

## Windows (PowerShell)

1. Open **PowerShell** and `cd` into the repository folder, e.g.:

   ```powershell
   cd $HOME\Documents\GitHub\SubstrateOS
   ```

2. Run the installer:

   ```powershell
   .\install.ps1
   ```

   If you see a red message about scripts being disabled, allow local scripts for
   your user once, then re-run:

   ```powershell
   Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
   .\install.ps1
   ```

3. **Open a NEW PowerShell window.** This matters, because your PATH only updates
   in fresh terminals. Then confirm the global command works from **any** folder:

   ```powershell
   subos --version          # works from any directory
   subos claude --dry-run   # previews a launch; starts no engine
   ```

   You should see a version like `SubstrateOS (subos) 0.2.0`. For a full environment
   report, run `labctl doctor` **from inside the project folder** (it inspects the
   repo), e.g.:

   ```powershell
   cd $HOME\Documents\GitHub\SubstrateOS
   labctl doctor
   ```

   You should see a list of green `[ok ]` checks. (The installer already ran this
   for you during install.)

---

## Linux and macOS

1. Open a terminal and `cd` into the repository folder:

   ```sh
   cd ~/SubstrateOS
   ```

2. Run the installer:

   ```sh
   ./install.sh
   ```

   (If you get "permission denied", run `chmod +x install.sh` once, then retry.)

3. **Open a new terminal** (so PATH refreshes), then confirm it works from **any**
   folder:

   ```sh
   subos --version          # works from any directory
   subos claude --dry-run   # previews a launch; starts no engine
   ```

   For a full environment report, run `labctl doctor` **from inside the project
   folder** (it inspects the repo):

   ```sh
   cd ~/SubstrateOS
   labctl doctor
   ```

If `subos` is still "command not found" in the new terminal, run `pipx ensurepath`
and open another new terminal, or add `~/.local/bin` to your PATH.

---

## First run

From **any** directory (you do not need to be inside the repository):

```sh
subos claude --dry-run
```

This previews what SubstrateOS will do: it compiles the canonical methodology into
the engine's instruction file and prints the launch plan, without starting the
engine. When you are ready to launch for real:

```sh
subos claude
```

Swap `claude` for `codex`, `gemini`, or `cursor` to use a different engine (you
must have that engine's command installed and on PATH; `labctl doctor` tells you
which engines it found).

---

## Optional: full-auto by default

By default SubstrateOS launches engines in their **safe** posture and you opt into
full-auto per run with `subos claude --full-auto`. If you want full-auto to be the
default on your machine, pass the opt-in flag to the installer:

```powershell
.\install.ps1 -FullAutoDefault          # Windows
```

```sh
./install.sh --full-auto-default        # Linux / macOS
```

This sets `SUBSTRATEOS_FULL_AUTO=1` in your **personal** user environment only. It
never changes the shared project. Reverse it any time by removing that variable
(Windows: `[Environment]::SetEnvironmentVariable("SUBSTRATEOS_FULL_AUTO",$null,"User")`;
Linux/macOS: delete the line from `~/.config/substrateos/overlay.env`). You can
also force the safe posture for a single run with `subos claude --platform-default`.

---

## Run in a container (advanced)

SubstrateOS ships a root `Dockerfile` that builds a "golden image": the same unit
can run locally and be deployed to a container platform (e.g. EKS). No secrets are
baked in; engine tokens are passed by environment-variable name at run time.

```sh
docker build -t substrateos:latest .
docker run --rm -it substrateos:latest labctl --help
```

---

## Upgrading and uninstalling

- **Upgrade:** pull the latest code and re-run the installer. It is idempotent and
  upgrades in place.
- **Uninstall:** `pipx uninstall labctl` (or delete the managed virtualenv under
  `~/.local/share/substrateos` / `%LOCALAPPDATA%\SubstrateOS` if the venv fallback
  was used).

---

## Troubleshooting

| Symptom | Fix |
| --- | --- |
| `subos: command not found` / not recognised | Open a **new** terminal. If still missing, run `pipx ensurepath` and open another, or add the bin directory the installer printed to your PATH. |
| "Python >= 3.11 required" | Install/upgrade Python from <https://www.python.org/downloads/>; on Windows tick "Add to PATH". |
| PowerShell "running scripts is disabled" | `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`, then re-run. |
| `labctl doctor` shows `[WARN]` lines | Warnings are advisory (optional tools/engines not found). Only `[FAIL]` is a hard error. |
| `subos: canonical spec not found` | Re-run the installer; the spec ships inside the package, so this means the install is incomplete. |
| Engine won't launch (`engine binary not on PATH`) | Install the engine's CLI (e.g. `claude`) and make sure it is on PATH; confirm with `labctl doctor`. |

Still stuck? Run `labctl doctor` and `labctl status`. Between them they describe
your environment and the next recommended action.
