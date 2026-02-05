!#/bin/bash
python3 -m venv ~/Library/env
source ~/Library/env/bin/activate
pip install --upgrade pip
pip install spidev mfrc522 snipeit
cp Library-IMS/Library.Desktop ~/Desktop/Library.Desktop
chmod u+x ~/Desktop/Library.Desktop
mv ~/Library/Library-IMS/Assets.py ~/Library/env/lib/python3.13/site-packages/snipeit/
mv ~/Library/Library-IMS/Users.py ~/Library/env/lib/python3.13/site-packages/snipeit/