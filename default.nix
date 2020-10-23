with (import <nixpkgs>{});

let
  app_name = "lig";
  app_version = "1.0";
in {
  ctrl_email = python37Packages.buildPythonPackage rec {
    name = "${app_name}";
    version = "${app_version}";

    src = fetchTarball("https://github.com/GuilloteauQ/lig_annuaire/tarball/main");
    propagatedBuildInputs = with python37Packages; [
      requests
      beautifulsoup4
      pybase64
      tabulate
    ];

    doCheck = false;

    postInstall = ''
      cp -r app/ $out
    '';
  };
}
