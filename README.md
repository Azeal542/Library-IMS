# Raspberry Pi setup

Currently the Library checkout system is running on 8GB models of the Raspberry Pi 4 set up with 16GB Optane SSDs.

### Part list

<table border="0" cellpadding="0" cellspacing="0" id="bkmrk-rfid-rc522-reader-1-" style="border-collapse: collapse; width: 205px; height: 165.781px;" width="204"><colgroup><col style="width: 140px;" width="140"></col><col style="width: 64px;" width="64"></col></colgroup><tbody><tr style="height: 29.7969px;"><td height="20" style="height: 29.7969px; width: 105pt;" width="140">RFID RC522 reader</td><td align="right" style="width: 48pt; height: 29.7969px;" width="64">1</td></tr><tr style="height: 29.7969px;"><td height="20" style="height: 29.7969px;">POE Splitter</td><td align="right" style="height: 29.7969px;">1</td></tr><tr style="height: 29.7969px;"><td height="20" style="height: 29.7969px;">M.2 NVMe adapter</td><td align="right" style="height: 29.7969px;">1</td></tr><tr style="height: 29.7969px;"><td height="20" style="height: 29.7969px;">Optane SSD</td><td align="right" style="height: 29.7969px;">1</td></tr><tr style="height: 46.5938px;"><td height="20" style="height: 46.5938px;">Female to Female jumper cables</td><td align="right" style="height: 46.5938px;">7

</td></tr><tr><td>7mm Thickness Embedded Heatsink with Fan</td><td>1

</td></tr><tr><td>3D printed Case</td><td>1

</td></tr></tbody></table>

## Setup process

### Image SD Card

1. Download and install the Raspberry Pi Imager  
    [https://downloads.raspberrypi.com/imager/imager\_latest.exe](https://downloads.raspberrypi.com/imager/imager_latest.exe)
2. Select the correct Raspberry Pi device
3. Select Raspberry Pi OS (64-bit)
4. Select the SD card
5. Enter hostname as \[Location\]Library
6. Set Localization
7. Set Username to kfheadstart
8. Set the password and add it to an entry in Bitwarden
9. Connect to the desired WiFi
10. Turn on SSH using password authentication
11. Ensure Raspberry Pi connect is set to off
12. Write to SD

### Assembly

GPIO diagram reference  
[https://pinout.xyz/](https://pinout.xyz/)

1. Insert imaged SD card into the Raspberry Pi
2. Cut thermal pads to size for CPU and RAM
3. Place cut thermal pads on CPU and RAM
4. Press and hold heatsink then flip Raspberry Pi to the bottom up
5. Screw in 7mm standoffs into the heatsink from the bottom.
6. Plug fan cable red side into pin 4 and black side into pin 6
7. Install Optane SSD into NVME adapter
8. Flip RasPi over so standoffs are facing up
9. Align NVME adapter holes with the standoffs with the SSD on the top
10. Screw in additional 7mm standoffs through the NVME adapter
11. Align plexiglass holes with standoffs then insert screw it in to the standoffs.
12. Flip RasPi over to see the top of the heatsink
13. Insert USB into the bottom port of the middle RasPi USB port and the NVME adapter

### Configuration

1. Boot RasPi and login
2. Run the following commands ```bash
    sudo apt update
    sudo apt upgrade -y
    mkdir Library
    cd Library
    git clone https://github.com/Azeal542/Library-IMS
    ./Library-IMS/builder.sh
    ```
3. Run sudo raspi-conifg
4. Select Interfacing options and press enter
5. Select SPI and enable it
6. Place the API key for Snipe-IT at <div><div>/home/kfheadstart/Documents/api.txt</div></div>
7. Run the SD card copier utility and duplicate the SD card to the SSD
8. Shut down the Raspberry Pi and remove the SD card
9. Boot the RasPi and verify that it is now booting from the SSD

### Final Assembly

1. Insert Raspberry Pi Assembly into the bottom half of the case
2. **SDA** connects to **Pin 24**
3. **SCK** connects to **Pin 23**
4. **MOSI** connects to **Pin 19**
5. **MISO** connects to **Pin 21**
6. **GND** connects to **Pin 20**
7. **RST** connects to **Pin 22**
8. **3.3v** connects to **Pin 17**
9. Carefully slide RFID board into the slot in the lid of the case
10. Close the lid
11. Assembly is now complete

### Final Test

1. Run the application shortcut on the desktop to ensure the application boots
2. Test the ID reader by tapping your ID on the top of the case
3. Test Check-in and Check-out features to verify everything is working
