# macup
An extremely minimal single-script offline Linux command line utility for matching MAC address prefixes to their vendors (and some other stuff)

---
# What is it?
macup (MAC Lookup) is a very small single-script command line tool intended to be used with Linux. macup allows you to match a 6-digit hex code MAC prefix to the vendor that owns that prefix. It also allows you to fetch all prefixes associated with a specific vendor, and to generate a random registered prefix for device spoofing. macup is extremely easy to use (it only has five command line options) and provides a versatile and very quick alternative to manually searching the prefix up on the Internet. In fact, it doesn't even require internet! Only once after install is internet required, during which macup is fetching the local database. Once this is done, you may continue on using macup without internet. This is very useful for checking if firewall-level MAC address blocks are working properly/whether they can be subverted via a MAC change. 

# Installation
## Arch Linux
macup is available on the AUR (Arch User Repository). install it with your preferred AUR helper, or build it from source:
```
yay -Sy macup
```
## Fedora/RHEL/CentOS
macup is available on Fedora's Copr repository and can be installed with `dnf`:
```
sudo dnf copr enable 3xiondev/macup
sudo dnf install macup
```
## Other Linux distributions
Prebuilt binaries are available on the Releases page. The tarball must be extracted and once that is done the binary can be found in `/dist`. Place the binary in `/usr/bin` and make it executable like so:
```
sudo chmod a+x macup
sudo mv macup /usr/bin
```

# Usage
before using macup for the first time, you need to initialize it. this requires a network connection and superuser privileges, though this is the last time either are needed. simply run:
```
sudo macup -i
```
and the utility will fetch the database and store it. once the database has been fetched, a network connection is no longer necessary.

you can check the syntax of macup with:
```
macup -h
```
though i will provide it and some examples here for clarity.

syntax:
```
macup <-pvrihs> <prefix/vendor>
-p | specify a prefix to return the vendor for
-v | specify a vendor to return all prefixes for
-r | return a random prefix and its vendor
-i | download the database that is necessary for macup's operation
-s | save output to specified filename (only works with -v, do not include file extension)
-h | display help message
```
for example, to search a prefix:
```
macup -p E8:F4:08
>>> E8:F4:08 | Intel Corporate
```
now to search a vendor:
```
macup -v Apple
>>> {a list of prefixes too long to place here}
```
finally, picking a random prefix:
```
macup -r
>>> 00:59:DC | Cisco Systems, Inc
```
