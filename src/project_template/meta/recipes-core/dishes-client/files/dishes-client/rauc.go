package main

import (
	"log"

	"github.com/holoplot/go-rauc"
)

/*
func example() {
	raucInstaller, err := rauc.InstallerNew()
	if err != nil {
		log.Fatal("Cannot create RaucInstaller")
	}

	operation, err := raucInstaller.GetOperation()
	if err != nil {
		log.Fatal("GetOperation() failed")
	}
	log.Printf("Operation: %s", operation)

	bootSlot, err := raucInstaller.GetBootSlot()
	if err != nil {
		log.Fatal("GetBootSlot() failed")
	}
	log.Printf("Boot slot: %s", bootSlot)

	slotStatus, err := raucInstaller.GetSlotStatus()
	if err != nil {
		log.Fatal("GetSlotStatus() failed")
	}

	for count, status := range slotStatus {
		log.Printf("status[%d]: %s", count, status.SlotName)

		for k, v := range status.Status {
			log.Printf("    %s: %s", k, v.String())
		}
	}

	variant, err := raucInstaller.GetVariant()
	if err != nil {
		log.Fatal("GetVariant() failed")
	}
	log.Printf("Variant: %s", variant)

	percentage, message, nestingDepth, err := raucInstaller.GetProgress()
	if err != nil {
		log.Fatal("GetProgress() failed", message)
	}
	log.Printf("Progress: percentage=%d, message=%s, nestingDepth=%d", percentage, message, nestingDepth)

	filename := "/data/update-bundle-raspberrypi4.raucb"
	compatible, version, err := raucInstaller.Info(filename)
	if err != nil {
		log.Fatal("Info() failed", err.Error())
	}
	log.Printf("Info(): compatible=%s, version=%s", compatible, version)

	err = raucInstaller.InstallBundle(filename, rauc.InstallBundleOptions{})
	if err != nil {
		log.Fatal("InstallBundle() failed: ", err.Error())
	}
}
*/

func Install(filename string) error {
	raucInstaller, err := rauc.InstallerNew()
	if err != nil {
		return err
	}

	operation, err := raucInstaller.GetOperation()
	if err != nil {
		return err
	}
	log.Printf("Operation: %s", operation)

	bootSlot, err := raucInstaller.GetBootSlot()
	if err != nil {
		return err
	}
	log.Printf("Boot slot: %s", bootSlot)

	slotStatus, err := raucInstaller.GetSlotStatus()
	if err != nil {
		return err
	}

	for count, status := range slotStatus {
		log.Printf("status[%d]: %s", count, status.SlotName)

		for k, v := range status.Status {
			log.Printf("    %s: %s", k, v.String())
		}
	}

	variant, err := raucInstaller.GetVariant()
	if err != nil {
		return err
	}
	log.Printf("Variant: %s", variant)

	percentage, message, nestingDepth, err := raucInstaller.GetProgress()
	if err != nil {
		return err
	}
	log.Printf("Progress: percentage=%d, message=%s, nestingDepth=%d", percentage, message, nestingDepth)

	compatible, version, err := raucInstaller.Info(filename)
	if err != nil {
		return err
	}
	log.Printf("Info(): compatible=%s, version=%s", compatible, version)

	err = raucInstaller.InstallBundle(filename, rauc.InstallBundleOptions{})
	if err != nil {
		return err
	}

	for count, status := range slotStatus {
		log.Printf("status[%d]: %s", count, status.SlotName)

		for k, v := range status.Status {
			log.Printf("    %s: %s", k, v.String())
		}
	}

	return nil
}
