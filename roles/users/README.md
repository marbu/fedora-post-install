# Users

This role creates local unix user accounts for main and additional users (if
any), as specified in variables:

* `main_user_name` (mandatory)
* `main_user_comment` (optional)
* `additional_users` (list of usernames, see defaults)
* `do_not_access_home_dir` (`False` by default)
