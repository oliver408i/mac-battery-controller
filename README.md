# MacOS Battery Charging Controller
This is a GUI for [battery](https://github.com/actuallymentor/battery) (a CLI-based MacOS charging controller) by actuallymentor   
The above program does contain a GUI app for controlling the battery (a wrapper for the CLI basically) but it is very limited in its features, only being able to enable and disable the 80% battery charge limit, which is a shame because the CLI version has so much more to offer.   
  
**Download in Releases**
  
## GUI Features
- Displays the battery charging state
- Output log directly from the CLI
- Enter any targeted percentage
- Charge and discharge to any percentage
- Maintain the battery at any percentage
- Enable and disable battery charging
<img width="551" alt="image" src="https://github.com/oliver408i/mac-battery-controller/assets/75344601/ea7db501-6e93-4c65-b6b3-b501f8c6812a">

## Building
**Requirements**    
You need py2app and create-dmg to build this yourself. Of course, you also need Python3. I used Python 3.10 but 3.8+ should work fine.   
Make sure setuptools is installed (it comes with most recent Python3 versions). Brew is required for create-dmg, but you can just download the pre-built binary from its github and put it in the same folder.
```
pip3 install -U py2app
brew install create-dmg
```
**Build the app (DevMode)**    
To test the app without making a dmg or bundling Python, do
```
python3 setup.py py2app
```
and say "y" for the devmode question and put down a version number. Find the built app in `dist`   
**Build the app (Production)**    
Do
```
python3 setup.py py2app
```
but say "n" for the devmode question. This one will take longer, and when the dmg is building, do not close the finder window that pops up automatically! It will close by itself.    
Wait until everything is done. The production app is in `dist` and the dmg should be in the main directory.

## Credits
Of course, this would never be possible without [battery](https://github.com/actuallymentor/battery)! Thanks to actuallymentor for making this excellent program!   
This app is made in Python 3.10 and compiled using [py2app](https://github.com/ronaldoussoren/py2app) and the DMGs are made with [create-dmg](https://github.com/create-dmg/create-dmg)
