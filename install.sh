#!/usr/bin/bash
# Script for install cronomaster from source in any linux distro
cronomaster_dir=/usr/cronomaster/
timeout=3
graphical="${cronomaster_dir}src/graphics/cronomaster_gtk.py"
graphical_command="/usr/bin/cronomaster_gtk"
terminal="${cronomaster_dir}src/cronomaster.py"
terminal_command="/usr/bin/cronomaster"
# Need root permissions
echo -e "\tINSTALLING [CRONOMASTER]"
sleep $timeout
echo -e "\nCopy files to ${cronomaster_dir} folder..."
mkdir -p $cronomaster_dir && cp -R "./" "${cronomaster_dir}"
chmod -R 666 $cronomaster_dir
sleep $timeout
echo "Making ${graphical} and ${terminal} executable..."
chmod 755 $graphical && chmod 755 $terminal
sleep $timeout
# Create commands for run in bash terminal
echo "Generating commands..."
echo -e "#\!/usr/bin/bash\n${graphical}" >> $graphical_command && echo -e "#\!/usr/bin/bash\n${terminal}" >> $terminal_command
# Make executuble the commands
chmod 755 $graphical_command && chmod 755 $terminal_command
sleep $timeout
echo -e "\n\tNow you could use 'cronomaster_gtk' and 'cronomaster' commands.\n"