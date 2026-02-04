!#/bin/bash
python3 -m venv ~/Library/env
source ~/Library/env/bin/activate
pip install --upgrade pip
pip install spidev mfrc522
cp Library-IMS/Library.desktop ~/Desktop/Library.desktop
chmod u+x ~/Desktop/Library.desktop