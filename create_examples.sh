#!/bin/bash

############################################################
# Help                                                     #
############################################################
Help()
{
   # Display Help
   echo "Creates the examples for the attack graphs."
   echo
   echo "Syntax: create_examples [-o|h]"
   echo "options:"
   echo "-o     Override examples."
   echo "-h     Print this Help."
   echo
}

override=0
while getopts ":ho" option; do
   case $option in
      h) # display Help
         Help
         exit;;
      o) #override
         override=1
         ;;
   esac
done

# Creating examples
# Atsea Path
ATSEA_PATH="examples/atsea"
# Javaee Path
JAVAEE_PATH="examples/javaee"
# Samba Path
SAMBA_PATH="examples/example/samba"
# Phpmailer Path
PHPMAILER_PATH="examples/example/phpmailer"
# Netflix OSS example Path
NETFLIX_PATH="examples/netflix-oss-example"

if [ "$override" = 1 ]; then
    echo "Erasing all folders of examples"
    if [ -d "$ATSEA_PATH" ]; then
        rm -r $ATSEA_PATH
    fi

    if [ -d "$JAVAEE_PATH" ]; then
        rm -r $JAVAEE_PATH
    fi

    if [ -d "$SAMBA_PATH" ]; then
        rm -r $SAMBA_PATH
    fi

    if [ -d "$PHPMAILER_PATH" ]; then
        rm -r $PHPMAILER_PATH
    fi

    if [ -d "$NETFLIX_PATH" ]; then
        rm -r $NETFLIX_PATH
    fi
fi



echo "Loading examples"
#Atsea
if ! [ -d "$ATSEA_PATH" ]; then
    unzip examples/atsea-sample-shop-app-master.zip -d examples
    sudo chmod -R 777 examples/atsea-sample-shop-app-master
    mv examples/atsea-sample-shop-app-master examples/atsea
fi

# Javaee
if ! [ -d "$JAVAEE_PATH" ]; then
   unzip examples/javaee-demo-master.zip -d examples
   sudo chmod -R 777 examples/javaee-demo-master
   mv examples/javaee-demo-master examples/javaee
fi

# Samba
if ! [ -d "$SAMBA_PATH" ]; then
    unzip examples/exploit-CVE-2017-7494-master -d examples
    sudo chmod -R 777 examples/exploit-CVE-2017-7494-master
    mv examples/exploit-CVE-2017-7494-master examples/example/samba
fi

# Phpmailer
if ! [ -d "$PHPMAILER_PATH" ]; then
    unzip examples/exploit-CVE-2016-10033-master -d examples
    sudo chmod -R 777 examples/exploit-CVE-2016-10033-master
    mv examples/exploit-CVE-2016-10033-master examples/example/phpmailer
fi

# Netflix OSS example
if ! [ -d "$NETFLIX_PATH" ]; then
    unzip examples/netflix-oss-example-master-modified -d examples
    sudo chmod -R 777 examples/netflix-oss-example-master-modified
    mv examples/netflix-oss-example-master-modified examples/netflix-oss-example
fi
