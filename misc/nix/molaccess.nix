{
  symlinkJoin,
  molaccess_python,
  molaccess_core,
}:
symlinkJoin {
  name = "molaccess";

  paths = [
    molaccess_core
    molaccess_python
  ];
}
