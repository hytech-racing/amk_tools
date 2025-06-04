{
  description = "Flake with devshell including ethercat";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs"; # Use unstable for better package availability
    nebs-packages.url = "github:RCMast3r/nebs_packages";
    nebs-packages.inputs.nixpkgs.follows = "nixpkgs";
  };

  outputs = { self, nixpkgs, nebs-packages }:
    let
      ethercat_tester_overlay = final: prev: {
        ethercat_tester = final.callPackage ./default.nix { };
      };

      my_overlays = [ 
        ethercat_tester_overlay
        nebs-packages.overlays.default 
      ];
      pkgs = import nixpkgs { 
        overlays = my_overlays;
        system = "x86_64-linux"; 
      };

    in {
      devShells.x86_64-linux.default = pkgs.mkShell {
        name = "ethercat-shell";
        inputsFrom = [ pkgs.ethercat_tester];
        # buildInputs = [
        #   pkgs.ethercat # Add ethercat package
        #   pkgs.ethercat_tester
        # ];

        shellHook = ''
          echo "Development shell with EtherCAT tools ready!"
        '';
      };
    };
}
