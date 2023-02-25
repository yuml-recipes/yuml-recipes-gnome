application_id = 'org.yumlrecipes.yumlrecipes'

x256_dir = join_paths('hicolor', '256x256', 'apps')
install_data(
  join_paths(x256_dir, ('@0@.png').format(application_id)),
  install_dir: join_paths(get_option('datadir'), 'icons', x256_dir)
)

scalable_dir = join_paths('hicolor', 'scalable', 'apps')
install_data(
  join_paths(scalable_dir, ('@0@.svg').format(application_id)),
  install_dir: join_paths(get_option('datadir'), 'icons', scalable_dir)
)

symbolic_dir = join_paths('hicolor', 'symbolic', 'apps')
install_data(
  join_paths(symbolic_dir, ('@0@-symbolic.svg').format(application_id)),
  install_dir: join_paths(get_option('datadir'), 'icons', symbolic_dir)
)
