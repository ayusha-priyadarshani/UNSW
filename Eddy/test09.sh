#!/bin/dash

############################################################################################################
#
#                                       ASSIGNMENT 1 - COMP2041
#                                            TEST SCRIPT 09
#                                               SUBSET 2
#
#                                       by  Ayusha Priyadarshani
#                                               z5452643
#
#                                              23-04-2024
#                    
############################################################################################################
#Tests eddy c features and errors 

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

echo "\teddy a"

#test05-1 
#Call eddy c

cat > "$expected_output" <<EOF
1
2
3
hello
5
EOF

seq 1 5 | eddy.py '4c hello' > "$actual_output" 2>&1

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
#Call eddy c with $

cat > "$expected_output" <<EOF
1
2
3
hello
5
EOF

seq 1 5 | eddy.py '$c hello' > "$actual_output" 2>&1

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

#-------------------------------------------------------------------------------------

#test05-3
#Call eddy c with no number

cat > "$expected_output" <<EOF
hello
hello
hello
hello
hello
EOF

seq 1 5 | eddy.py 'c hello' > "$actual_output" 2>&1

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
    echo "test05-3: ${Green}Passed test${No_colour}"
    count=$((count+1))
fi

if [ $count -eq 3 ]
then 
    exit 0
fi
