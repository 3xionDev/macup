# macup
An extremely minimal single-script offline Linux command line utility for matching MAC address prefixes to their vendors (and some other stuff)

---
# What is it?
macup (MAC Lookup) is a very small single-script command line tool intended to be used with Linux. macup allows you to match a 6-digit hex code MAC prefix to the vendor that owns that prefix. It also allows you to fetch all prefixes associated with a specific vendor, and to generate a random registered prefix for device spoofing. macup is extremely easy to use (it only has five command line options) and provides a versatile and very quick alternative to manually searching the prefix up on the Internet. In fact, it doesn't even require internet! Only once after install is internet required, during which macup is fetching the local database. Once this is done, you may continue on using macup without internet. This is very useful for checking if firewall-level MAC address blocks are working properly/whether they can be subverted via a MAC change. 

# Installation
## Arch Linux
macup is available on the AUR (Arch User Repository). install it with your preferred AUR helper, or build it from source:
```
yay -S macup
```
## Other Linux distributions
macup is so simple that I was able to fit everything into one install script. this means that installation is incredibly easy. this is the procedure for installation (you need internet for this):
```
git clone https://github.com/3xiondev/macup.git
cd macup
```
the install script is marked as nonexecutable by default, so we need to make it executable:
```
chmod +x install.sh
```
finally, we run the script with sudo. do not run the script as root user:
```
sudo ./install.sh
```
Once the process has finished, congratulations! macup is ready. however, you're not done setting it up. read on for further instructions.

# Usage
before using macup for the first time, you need to intialize it. this requires a network connection, though this is the last time internet is needed. simply run:
```
macup -i
```
and the utility will fetch the database and store it. once the database has been fetched, a network connection is no longer necessary.

you can check the syntax of macup with:
```
macup -h
```
though i will provide it and some examples here for clarity.

syntax:
```
macup <-pvrih> <prefix/vendor>
-p | specify a prefix to return the vendor for
-v | specify a vendor to return all prefixes for
-r | return a random prefix and its vendor
-i | download the database that is necessary for macup's operation
-h | display help message
```
for example, to search a prefix:
```
macup -p E8:F4:08
>>> Intel Corporate
```
now to search a vendor:
```
macup -v Apple
>>> {a list of prefixes too long to place here}
```
finally, picking a random prefix:
```
macup -r
>>> 00:59:DC Cisco Systems, Inc
```
