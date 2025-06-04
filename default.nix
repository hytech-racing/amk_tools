{ pkgs, stdenv, cmake, ... }:
stdenv.mkDerivation {
  pname = "SOEM";
  version = "0.0.1";
  src = ./ethercat_tester;
  nativeBuildInputs = [ cmake pkgs.soem ];
}