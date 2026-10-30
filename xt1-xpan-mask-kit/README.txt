X-T1 XPan Mask - patch kit (experimental)
==========================================

Turns the Fujifilm X-T1's "HD Framing" guideline into a 65:24 (XPan) mask in the viewfinder and on the LCD screen.

Photos are not cropped: shoot in L 3:2 and crop to 4896 x 1808 on import.

USE AT YOUR OWN RISK. This modifies camera firmware. It has been tested on one
camera. A bad flash could leave your camera unusable. Not affiliated with or
endorsed by Fujifilm. No warranty of any kind.

You need
  - A Fujifilm X-T1
  - The official X-T1 firmware 5.52 file (FWUP0005.DAT) from Fujifilm
  - Python 3
  - An SD card and a fully charged battery

Make the patched file
  Move FWUP0005.DAT into this folder, open a terminal here, and run:

  python3 patch_dat.py FWUP0005.DAT out/FWUP0005.DAT xpan-mask.patch

  The script refuses to write anything unless your input file is exactly the
  official 5.52 file. Expected:
    input  sha256 4cf56ba6abb4298a844422c016289228bb0acce0a2ae2c6755c05fffb38e92db
    output sha256 f4ba1f041f795e30617443c15d964d862d1195a79acce622c94d8f38784c700b

Install
  1. Copy out/FWUP0005.DAT to the root of a freshly formatted SD card
  2. Switch the framing guideline setting to the default "Grid 9" and set Image Size to L 3:2
  3. Run the firmware update by holding DISP / BACK and powering on the camera, as described in Fujifilm's instructions
  4. Set framing guideline to "HD Framing"

Undo
  Flash the unmodified official FWUP0005.DAT the same way.
