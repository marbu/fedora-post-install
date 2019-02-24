# Gitit Personal Wiki

Setup [gitit](http://github.com/jgm/gitit/tree/master/) as a personal wiki for
`gitit_username` user via
[systemd user session](https://wiki.archlinux.org/index.php/Systemd/User).

The role also creates firewall rule which prevents all unix users but
`gitit_username` to access tcp port `gitit_port` where the wiki is running.
When `firewall_type` is `firewalld`, this is done via [firewalld direct
rules](https://firewalld.org/documentation/man-pages/firewalld.direct).
Unfortunatelly, [ansible firewalld
module](https://docs.ansible.com/ansible/latest/modules/firewalld_module.html)
[doesn't support this](https://github.com/ansible/ansible/issues/21439) right
now.

References:

* [Gitit as my personal wiki](https://nathantypanski.com/blog/2014-07-09-personal-wiki.html)
* [All your daemons are belong to us](https://nathantypanski.com/blog/2014-07-25-all-your-daemons.html)
* Systemd [service files are not part of upstream
  gitit source code](https://github.com/jgm/gitit/issues/503)
* [Firewalld: Using the Direct Interface](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/security_guide/using_the_direct_interface)
