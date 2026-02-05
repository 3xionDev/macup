#!/bin/bash

echo "----------------------------------------------------"
echo "macup: an open-source offline MAC prefix lookup tool"
echo "Nolan Stone (3xiondev) 2026"
echo "----------------------------------------------------"
echo "Beginning install..."
echo "Finding kernel distribution..."
if [[ -e "/usr" ]]; then
	if [[ -f /etc/os-release ]]; then
		echo "Kernel found!"
    		# On Linux systems, source the file to load variables like ID and PRETTY_NAME
    		source /etc/os-release
		echo "Linux distribution: $PRETTY_NAME"
    		echo "ID: $ID"
	elif [[ "$(uname)" == "Darwin" ]]; then
    		echo "macOS detected."
	else
    		echo "OS is not Linux or macOS."
	fi
	
	echo "Installing dependencies..."
	if [[ $ID_LIKE == *"debian"* || $ID == "debian" ]]; then
		sudo apt install jq wget
	elif [[ $ID_LIKE == *"fedora"* || $ID == "fedora" ]]; then
		sudo dnf install jq wget
	elif [[ $ID_LIKE == *"arch"* || $ID == "arch" ]]; then
		sudo pacman -S jq wget
	else
		echo "This script doesn't support your package manager. Please manually install jq and wget."
	fi


	sudo mkdir -p /usr/local/lib/macup
	cat > /usr/local/bin/macup <<EOL
	#!/bin/bash
	
	if [[ "\$#" -eq 0 ]]; then
		echo "This utility requires arguments. Run macup -h to for how to use this command."
	fi
	
	if [[ "\$1" == "-h" ]]; then
		echo "macup is a (mostly) offline lookup tool for MAC address prefixes and their respective vendors."
		echo "Syntax: macup <-pvrih> <prefix/vendor>"
		echo "Options:"
		echo "-i | Initializes the utility and downloads the database. This is the only time macup requires a network connection."
		echo "-p | Specify a prefix and return the vendor associated with that prefix"
		echo "-v | Specify a vendor and return all associated prefixes"
		echo "-s | Only return values strictly adhering to specified vendor name when -v is used"
		echo "-r | Generate a random prefix and its vendor (for subversion testing purposes)"
		echo "-h | Display this message and end execution"
	fi
	
	if [[ "\$1" == "-i" && "\$#" -eq 1 ]]; then
		echo "Fetching database..."
		sudo mkdir -p /usr/local/lib/macup
		sudo wget -O /usr/local/lib/macup/mac-vendor.json "https://maclookup.app/downloads/json-database/get-db"
	fi
	
	DPATH="/usr/local/lib/macup"
	
	if [[ "\$1" == "-p" && -e "\$DPATH/mac-vendor.json" ]]; then
		jq -r --arg val "\$2" '.[] | select(.["macPrefix"]? == \$val) | .["vendorName"]' "\$DPATH/mac-vendor.json"
	fi

	if [[ "\$1" == "-v" && -e "\$DPATH/mac-vendor.json" ]]; then
		jq -r --arg val "\$2" '
	  	.[]
	  	| select(.["vendorName"]? | contains(\$val))
	  	| "\(.macPrefix) \(.vendorName)"
		' "\$DPATH/mac-vendor.json"
	fi

	if [[ "\$1" == "-vs" && -e "\$DPATH/mac-vendor.json" ]]; then
		jq -r --arg val "\$2" '
		.[]
		| select(.["vendorName"] == \$val)
		| "\(.macPrefix) \(.vendorName)"
		' "\$DPATH/mac-vendor.json"
	fi

	if [[ "\$1" == "-r" && -e "\$DPATH/mac-vendor.json" ]]; then
	        count=\$(jq 'length' "\$DPATH/mac-vendor.json")
		index=\$(shuf -i 0-\$((count - 1)) -n 1)
	        jq -r ".[\$index] | \"\(.macPrefix) \(.vendorName)\"" "\$DPATH/mac-vendor.json"
	fi
EOL
	chmod +x /usr/local/bin/macup
	echo "Finished! Run macup -h to test if it works."
else
	echo "No Linux kernel detected! This is a Linux-only utility. Sorry!"
fi


