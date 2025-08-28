#!/usr/bin/bash
# Script for install in any distro

cronomaster_dir=/usr/cronomaster/
timeout=3
graphical="${cronomaster_dir}/src/graphics/cronomaster_gtk.py"
terminal="${cronomaster_dir}/src/cronomaster.py"

sudo -k mkdir $cronomaster_dir
echo "Copy files to ${cronomaster_dir} folder..."
cp -R ./ $cronomaster_dir
sleep $timeout
echo "Making ${graphical} and ${terminal} executable..."
chmod 755 $graphical
chmod 755 $terminal
sleep $timeout
# This part need root privileges using su session
echo "Generating commands..."
sudo su
echo -e "#\!/usr/bin/bash\n${graphical}" >> /usr/bin/cronomaster_gtk
echo -e "#\!/usr/bin/bash\n${terminal}" >> /usr/bin/cronomaster
chmod 755 /usr/bin/cronomaster_gtk
chmod 755 /usr/bin/cronomaster
# End root privileges for security
sudo -k
sleep $timeout
echo "Now could use cronomaster_gtk and cronomaster commands."