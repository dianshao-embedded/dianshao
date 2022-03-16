# dishes-client-1.0.0
# Auto Generate by Dianshao
FILESEXTRAPATHS_prepend := "${THISDIR}/files:"
DESCRIPTION = "dishes client test"
LICENSE = "CLOSED"
DEPENDS = "go-native"
SRC_URI = "\ 
	file://dishes-client.service \
	file://dishes-client \
"
S = "${WORKDIR}/dishes-client"
inherit goarch systemd
SYSTEMD_AUTO_ENABLE = "enable"
SYSTEMD_SERVICE_${PN} = "dishes-client.service"
export HOME = "${WORKDIR}"
export GOOS = "${TARGET_GOOS}"
export GOARCH = "${TARGET_GOARCH}"
export GOARM = "${TARGET_GOARM}"
export GOCACHE = "${WORKDIR}/go/cache"
export GOPROXY = "https://goproxy.io,direct"
FILES_${PN} += "/etc/systemd/system"
do_compile () {
	go build
	go clean -modcache
}
do_install () {
	install -d ${D}/usr/bin
	install -m 0755 ${WORKDIR}/dishes-client/dishes-client ${D}/usr/bin
	install -d ${D}/etc/systemd/system
	install -m 0644 ${WORKDIR}/dishes-client.service ${D}/etc/systemd/system
}
