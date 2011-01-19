./init_cbdb
cd ../src
paster setup-app development.ini
nosetests
cd ../admin_scripts
# AllanC - I know there is a better way rather than using "cd" but I cant remeber it offhand

