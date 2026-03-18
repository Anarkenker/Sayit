#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
IMAGE_NAME="${SAYIT_IMAGE_NAME:-sayit}"

print_note() {
  printf '%s\n' "$1"
}

load_host_clipboard() {
  if [[ "${SAYIT_CLIPBOARD_TEXT+set}" == "set" ]]; then
    printf '%s' "$SAYIT_CLIPBOARD_TEXT"
    return 0
  fi

  case "$(uname -s)" in
    Darwin)
      command -v pbpaste >/dev/null 2>&1 || return 1
      pbpaste
      return $?
      ;;
    Linux)
      if command -v wl-paste >/dev/null 2>&1; then
        wl-paste --no-newline
        return $?
      fi
      if command -v xclip >/dev/null 2>&1; then
        xclip -selection clipboard -o
        return $?
      fi
      if command -v xsel >/dev/null 2>&1; then
        xsel --clipboard --output
        return $?
      fi
      ;;
    *)
      if command -v pwsh >/dev/null 2>&1; then
        pwsh -NoProfile -Command Get-Clipboard
        return $?
      fi
      if command -v powershell >/dev/null 2>&1; then
        powershell -NoProfile -Command Get-Clipboard
        return $?
      fi
      if command -v powershell.exe >/dev/null 2>&1; then
        powershell.exe -NoProfile -Command Get-Clipboard
        return $?
      fi
      ;;
  esac

  return 1
}

ensure_docker_cli() {
  if ! command -v docker >/dev/null 2>&1; then
    print_note "Docker is not installed. Please install Docker Desktop first."
    exit 1
  fi
}

ensure_env_file() {
  if [[ ! -f "$ROOT_DIR/.env" ]]; then
    cp "$ROOT_DIR/.env.example" "$ROOT_DIR/.env"
    print_note "Created $ROOT_DIR/.env from .env.example"
    print_note "Open .env and paste your key after OPENAI_API_KEY=, then run the command again."
    exit 1
  fi
}

bootstrap_env_file() {
  if [[ ! -f "$ROOT_DIR/.env" ]]; then
    cp "$ROOT_DIR/.env.example" "$ROOT_DIR/.env"
    print_note "Created $ROOT_DIR/.env from .env.example"
  fi
}

maybe_start_docker() {
  if docker info >/dev/null 2>&1; then
    return
  fi

  if [[ "$(uname -s)" == "Darwin" ]]; then
    print_note "Docker Desktop is not running. Trying to open it..."
    open -ga Docker >/dev/null 2>&1 || true
    for _ in {1..45}; do
      if docker info >/dev/null 2>&1; then
        print_note "Docker Desktop is ready."
        return
      fi
      sleep 2
    done
  fi

  print_note "Docker is still not available. Please start Docker Desktop and try again."
  exit 1
}

build_image() {
  local source_hash
  source_hash="$(image_source_hash)"
  print_note "Building Docker image '$IMAGE_NAME'..."
  docker build --label "sayit.source_hash=$source_hash" -t "$IMAGE_NAME" "$ROOT_DIR"
}

image_source_hash() {
  (
    cd "$ROOT_DIR"
    {
      shasum Dockerfile
      shasum pyproject.toml
      shasum README.md
      shasum README.zh-CN.md
      find src -type f | LC_ALL=C sort | while IFS= read -r file; do
        shasum "$file"
      done
    } | shasum | awk '{print $1}'
  )
}

image_needs_rebuild() {
  local current_hash
  local image_hash

  current_hash="$(image_source_hash)"
  image_hash="$(
    docker image inspect \
      -f '{{ index .Config.Labels "sayit.source_hash" }}' \
      "$IMAGE_NAME" 2>/dev/null || true
  )"

  [[ -z "$image_hash" || "$image_hash" != "$current_hash" ]]
}

ensure_image() {
  if ! docker image inspect "$IMAGE_NAME" >/dev/null 2>&1; then
    build_image
    return
  fi

  if image_needs_rebuild; then
    build_image
  fi
}

docker_run_flags() {
  if [[ -t 0 && -t 1 ]]; then
    printf '%s\n' "-it"
    return
  fi

  if [[ ! -t 0 ]]; then
    printf '%s\n' "-i"
  fi
}

env_value() {
  local key="$1"
  local value
  value="$(grep -E "^${key}=" "$ROOT_DIR/.env" | tail -n 1 | cut -d= -f2- || true)"
  printf '%s' "$value"
}

env_has_any_key() {
  local key
  for key in OPENAI_API_KEY OPENROUTER_API_KEY SAYIT_CUSTOM_API_KEY; do
    if [[ -n "$(env_value "$key")" ]]; then
      return 0
    fi
  done
  return 1
}

sayit_command_name() {
  printf '%s' "${SAYIT_COMMAND_NAME:-sayit}"
}

select_install_dir() {
  if [[ -n "${SAYIT_INSTALL_DIR:-}" ]]; then
    printf '%s' "$SAYIT_INSTALL_DIR"
    return
  fi

  local candidate
  local preferred_dirs=(
    "/opt/homebrew/bin"
    "/usr/local/bin"
    "$HOME/.local/bin"
    "$HOME/bin"
  )

  for candidate in "${preferred_dirs[@]}"; do
    [[ -d "$candidate" && -w "$candidate" ]] || continue
    if path_contains_dir "$candidate"; then
      printf '%s' "$candidate"
      return
    fi
  done

  printf '%s' "$HOME/.local/bin"
}

path_contains_dir() {
  local dir="$1"
  case ":${PATH:-}:" in
    *":$dir:"*) return 0 ;;
    *) return 1 ;;
  esac
}

path_config_file() {
  case "${SHELL##*/}" in
    zsh)
      if [[ "$(uname -s)" == "Darwin" ]]; then
        printf '%s' "$HOME/.zprofile"
      else
        printf '%s' "$HOME/.zshrc"
      fi
      ;;
    bash)
      printf '%s' "$HOME/.bashrc"
      ;;
    *)
      printf '%s' "$HOME/.profile"
      ;;
  esac
}

ensure_path_configured() {
  local install_dir="$1"
  local rc_file
  local export_line

  path_contains_dir "$install_dir" && return 0

  rc_file="$(path_config_file)"
  export_line="export PATH=\"$install_dir:\$PATH\""
  mkdir -p "$(dirname "$rc_file")"

  if [[ ! -f "$rc_file" ]] || ! grep -Fqx "$export_line" "$rc_file"; then
    printf '\n# sayit command\n%s\n' "$export_line" >> "$rc_file"
  fi

  print_note "Added $install_dir to PATH in $rc_file."
  print_note "Open a new terminal, or run:"
  print_note "  export PATH=\"$install_dir:\$PATH\""
}

install_shell_command() {
  local command_name
  local install_dir
  local launcher_path
  local launcher_target

  command_name="$(sayit_command_name)"
  install_dir="$(select_install_dir)"
  launcher_path="$install_dir/$command_name"
  launcher_target="$ROOT_DIR/sayit"

  mkdir -p "$install_dir"

  if [[ -f "$launcher_path" ]]; then
    if ! grep -Fq "# sayit launcher" "$launcher_path" 2>/dev/null; then
      print_note "A different command already exists at $launcher_path."
      print_note "Set SAYIT_INSTALL_DIR=... and run ./setup again if you want a different install location."
      return 1
    fi
  fi

  cat > "$launcher_path" <<EOF
#!/usr/bin/env bash
# sayit launcher
exec "$launcher_target" "\$@"
EOF
  chmod +x "$launcher_path"

  print_note "Installed '$command_name' to $launcher_path"

  if path_contains_dir "$install_dir"; then
    print_note "You can now run:"
    print_note "  $command_name \"你这个怎么还没弄完\""
  else
    ensure_path_configured "$install_dir"
    print_note "After reloading your shell, you can run:"
    print_note "  $command_name \"你这个怎么还没弄完\""
  fi
}
