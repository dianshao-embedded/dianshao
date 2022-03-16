package main

import (
	"flag"
	"fmt"
	"log"
	"os"
	"os/exec"
)

var baseUrl = flag.String("url", "http://127.0.0.1:10088", "Server API Address")
var interval = flag.Int("interval", 10, "Client Program Execution Interval")
var product_id = flag.String("product", "bar", "Device Product ID")
var device_id = flag.String("device", "foo", "Device Device ID")
var path = flag.String("path", ".", "Upgrade Package Storage Path")

func main() {
	flag.Parse()

	fmt.Println(*product_id)

	err := HttpClient(*baseUrl, *interval, *product_id, *device_id, *path)
	if err != nil {
		log.Println(err)
		os.Exit(1)
	}

	cmd := exec.Command("bash", "-c", "reboot")
	stdout, err := cmd.Output()
	if err != nil {
		log.Println(err)
		os.Exit(1)
	}

	log.Println(stdout)

	os.Exit(0)
}
