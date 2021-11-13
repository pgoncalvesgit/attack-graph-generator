#!/bin/bash


############################################################
# Help                                                     #
############################################################
Help()
{
   # Display Help
   echo "Creates the attack graphs."
   echo
   echo "Syntax: attack-graph-generator [-o|h]"
   echo "options:"
   echo "-o     Override examples."
   echo "-f <directory> Specify the directory to analyze."
   echo "-h     Print this Help."
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
             echo "-f usage: \"Specify the directory with the files\""
             exit
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





# Starts the generator
echo "The dependencies are installed. Starting the attack graph generator."
echo ""
sudo python3 main.py $input_directory

if  [ $1 == "--help" ]; then
    echo "Option --help turned on"
    echo "Command: ./attack-graph-generator.sh <example-folder-path> <goal-container>"
    echo "<example-folder-path> is the folder that we want to analyze."
    echo "<goal-container> is the name of the docker that the attacker wants to control."
fi



