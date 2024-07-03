#!/bin/dash

############################################################################################################
#
#                                       ASSIGNMENT 1 - COMP2041
#                                            TEST SCRIPT 05
#                                               SUBSET 0
#
#                                       by  Ayusha Priyadarshani
#                                               z5452643
#
#                                              22-04-2024
#                    
############################################################################################################
#Tests eddy -n features and errors 

#Add the current directory to the PATH so scripts
# can still be executed from it after we cd


PATH="$PATH:$(pwd)"

#Create a temporary directory for the test
test_dir="$(mktemp -d)"
cd "$test_dir" || exit 1

#Create some files to hold output

expected_output="$(mktemp)"
actual_output="$(mktemp)"


#Colours for output
Green='\033[0;32m'
Red='\033[0;31m'
No_colour='\033[0m'


#Remove the temporary directory when the test is done

trap 'rm "$expected_output" "$actual_output" -rf "$test_dir"' INT HUP QUIT TERM EXIT

#Count number of tests passed

count=0

#-------------------------------------------------------------------------------------

echo "\teddy -n"

#test05-1 
#Call eddy -n with a simple p command

cat > "$expected_output" <<EOF
4
EOF

seq 1 100 | eddy.py -n '4p' > "$actual_output" 2>&1

#Check if output produced matches the output expected

if ! diff "$expected_output" "$actual_output"; then
    echo "test05-1: ${Red}Failed test${No_colour}"
    echo "Your output:"
    echo ${Red}              
    cat "$actual_output"
    echo ${No_colour}
    echo "Expected output:"
    echo ${Green}              
    cat "$expected_output"
    echo ${No_colour}
    exit 1
else
    echo "test05-1: ${Green}Passed test${No_colour}"
    count=$((count+1))
fi

#-------------------------------------------------------------------------------------

#test05-2
#Call eddy -n with regex p command

cat > "$expected_output" <<EOF
20
23
26
29
EOF

seq 14 3 32 | eddy.py -n '/^2/p' > "$actual_output" 2>&1

#Check if output produced matches the output expected

if ! diff "$expected_output" "$actual_output"; then
    echo "test05-2: ${Red}Failed test${No_colour}"
    echo "Your output:"
    echo ${Red}              
    cat "$actual_output"
    echo ${No_colour}
    echo "Expected output:"
    echo ${Green}              
    cat "$expected_output"
    echo ${No_colour}
    exit 1
else
    echo "test05-2: ${Green}Passed test${No_colour}"
    count=$((count+1))
fi

if [ $count -eq 2 ]
then 
    exit 0
fi
