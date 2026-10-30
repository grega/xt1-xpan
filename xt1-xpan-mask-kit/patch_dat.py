"""Patch the X-T1 FWUP0005.DAT linear (uncompressed) region by RAM address.

Usage: python3 -I patch_dat.py <stock.DAT> <out.DAT> <patchfile>

Patch file lines:  <ram_addr> <old_hex> <new_hex>  [# comment]
                   sha256-in <hex>    (optional: required hash of the stock file)
                   sha256-out <hex>   (optional: expected hash of the result)
Bytes are logical (as they appear in RAM, little-endian instruction words).
Every old byte is checked against the stock file before anything is written.
"""
import hashlib
import os
import struct
import sys

HDR_CHECKSUM = 0x20c
PAYLOAD = 0x214
LINEAR_LO, LINEAR_HI = 0x1900000, 0x1e00000
RAM_TO_DAT = -0x123fda4   # DAT file offset = RAM + RAM_TO_DAT (linear region)


def load_patches(path):
    patches, hashes = [], {}
    for line in open(path):
        line = line.split('#', 1)[0].strip()
        if not line:
            continue
        if line.startswith('sha256-'):
            key, value = line.split()
            hashes[key] = value.lower()
            continue
        addr, old, new = line.split()
        addr = int(addr, 16)
        old, new = bytes.fromhex(old), bytes.fromhex(new)
        if len(old) != len(new):
            sys.exit(f'{addr:#x}: old/new length differ')
        if not (LINEAR_LO <= addr and addr + len(old) <= LINEAR_HI):
            sys.exit(f'{addr:#x}: outside the linear region')
        patches.append((addr, old, new))
    return patches, hashes


def main():
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    src, dst, spec = sys.argv[1:4]
    dat = bytearray(open(src, 'rb').read())
    patches, hashes = load_patches(spec)
    if 'sha256-in' in hashes:
        have = hashlib.sha256(dat).hexdigest()
        if have != hashes['sha256-in']:
            sys.exit(f'{src} is not the expected firmware file (sha256 {have}) - nothing written')
        print('stock file hash OK')
    checksum = struct.unpack_from('<I', dat, HDR_CHECKSUM)[0]
    print(f'stock checksum {checksum:#010x}')

    for addr, old, new in patches:
        off = addr + RAM_TO_DAT
        if off < PAYLOAD:
            sys.exit(f'{addr:#x}: maps into the header')
        have = bytes(b ^ 0xff for b in dat[off:off + len(old)])
        if have != old:
            sys.exit(f'{addr:#x}: expected {old.hex()} but stock has {have.hex()} - nothing written')

    for addr, old, new in patches:
        off = addr + RAM_TO_DAT
        dat[off:off + len(new)] = bytes(b ^ 0xff for b in new)
        checksum = (checksum + sum(old) - sum(new)) & 0xffffffff
        print(f'RAM {addr:#x}  DAT {off:#x}  {old.hex()} -> {new.hex()}')

    struct.pack_into('<I', dat, HDR_CHECKSUM, checksum)
    print(f'new checksum   {checksum:#010x}')
    if 'sha256-out' in hashes:
        have = hashlib.sha256(dat).hexdigest()
        if have != hashes['sha256-out']:
            sys.exit(f'result hash {have} does not match the expected hash - nothing written')
        print('result hash OK')
    if os.path.dirname(dst):
        os.makedirs(os.path.dirname(dst), exist_ok=True)
    open(dst, 'wb').write(dat)
    print(f'wrote {dst}')


if __name__ == '__main__':
    main()
