#!/bin/bash
set -o errexit
set -o pipefail
set -o nounset

caddy_version="2.7.5"
plat_os="linux"
plat_arch="amd64"
caddy_gz="caddy_${caddy_version}_${plat_os}_${plat_arch}.tar.gz"
caddy_release_url="https://github.com/caddyserver/caddy/releases/download/v${caddy_version}/${caddy_gz}"
work_dir="$(mktemp -d)"

echo "Download Caddy"
pushd "${work_dir}" || exit
curl -s -O -L "${caddy_release_url}"
tar xf ${caddy_gz} -C "${work_dir}"
mv "${work_dir}/caddy" /usr/bin/
popd || exit

echo "Clean up extra Caddy files"
rm "${caddy_gz}"

echo Enable Caddy to bind low ports
sudo setcap 'cap_net_bind_service=+ep' /usr/bin/caddy
