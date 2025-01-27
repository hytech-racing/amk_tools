{
  description = "Flake with devshell including ethercat";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs"; # Use unstable for better package availability
  };

  outputs = { self, nixpkgs }:
    let
      pkgs = import nixpkgs { system = "x86_64-linux"; };
    in {
      devShells.x86_64-linux.default = pkgs.mkShell {
        name = "ethercat-shell";

        buildInputs = [
          pkgs.ethercat # Add ethercat package
        ];

        shellHook = ''
          echo "Development shell with EtherCAT tools ready!"
        '';
      };
    };
}
