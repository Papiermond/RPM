let
  nixpkgs = fetchTarball "https://github.com/NixOS/nixpkgs/tarball/nixos-24.05";
  pkgs = import nixpkgs { config = {}; overlays = []; };
in

pkgs.mkShellNoCC {
  packages = with pkgs; [
    git
    neovim
    lunarvim
    python3
    nodePackages.nodejs  # includes npm
  ];

  shellHook = ''
    echo "[*] Setting up RPM development environment..."

    # Clone repo if missing
    if [ ! -d "$HOME/RPM" ]; then
      git clone https://github.com/Papiermond/RPM.git "$HOME/RPM"
    fi

    cd "$HOME/RPM"

    # Setup Python venv
    if [ ! -d ".venv" ]; then
      python3 -m venv .venv
    fi

    source .venv/bin/activate
    pip install --upgrade pip
    if [ -f  requirments.txt ]; then
      pip install -r  requirments.txt
    else
      echo "Warning: requirements.txt not found"
    fi

    # Setup npm prefix and install Vue CLI
    mkdir -p ~/.npm-global
    npm config set prefix ~/.npm-global
    export PATH="$HOME/.npm-global/bin:$PATH"
    npm install -g @vue/cli
    
    clear
    echo "[✔] Environment ready. Happy hacking!"
    nvim .
  '';
}
