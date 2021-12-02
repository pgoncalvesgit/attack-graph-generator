#!/bin/bash


############################################################
# Help                                                     #
############################################################
Help()
{
   # Display Help
   echo "Creates the attack graphs."
   echo
   echo "Syntax: attack-graph-generator -f <directory_to_analyze> [-o|h]"
   echo "options:"
   echo "-o     Override examples."
   echo "-f     <directory> Specify the directory to analyze."
   echo "-h     Print this Help."
   echo "-g     Goal container."
   echo
}

override=0
input_directory=""
while getopts ":hof:" option; do
   case $option in
      h) # display Help
         Help
         exit
         ;;
      o) #override
         #echo "entrou"
         override=1
         ;;
      f)
         f=${OPTARG}
         input_directory=$f
         if ! [ -d "$input_directory" ]; then
             echo "WARNING: Directory doesn't exist!"
             echo "-f usage: \"Specify the directory with the files\""
             echo
             echo "Unless it is an example and will be created during the execution of the program, I recommend you to stop the program!"
             while true; do
                 read -p "Do you still want to continue?(Y/y) for yes, and (N/n) for no." yn
                 case $yn in
                     [Yy]* ) break;;
                     [Nn]* ) exit;;
                     * ) echo "Please answer yes or no.";;
                 esac
             done
         fi
         ;;
   esac
done

#echo $input_directory
if [ -z "$input_directory" ]; then
    Help
    exit
fi



echo "Checking if dependencies are installed..."
echo
./download_dependencies.sh
echo
echo
echo




# Creating examples
echo "Creating examples..."
if [ "$override" = 1 ]; then
    ./create_examples.sh -o
else
    ./create_examples.sh
fi

if [ -z "$input_directory" ]; then
    echo "Directory given does not exist"
    echo "usage: -f <directory_to_analyze>"
    echo "\"Specify the directory with the files\""
    echo
    exit
fi



# Starts the generator
echo "The dependencies are installed. Starting the attack graph generator."
echo ""
sudo python3 main.py $input_directory


