{ pkgs ? import <nixpkgs> {} }:
let
  pyPkgs = pkgs.python3.withPackages (p: [
    p.flask
    p.pycryptodome
    p.pyjwt
    p.python-dotenv
    p.cryptography
    p.pyotp
  ]);
in
  pkgs.mkShell {
    nativeBuildInputs = with pkgs.buildPackages; [
      pyPkgs
    ];
}

