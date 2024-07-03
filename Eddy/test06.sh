#!/bin/dash

############################################################################################################
#
#                                       ASSIGNMENT 1 - COMP2041
#                                            TEST SCRIPT 06
#                                               SUBSET 1
#
#                                       by  Ayusha Priyadarshani
#                                               z5452643
#
#                                              24-03-2024
#                    
############################################################################################################
#Tests some advanced eddy s features and errors 

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

echo "\teddy s - advanced"

#test06-1 
#Call eddy s with _ instead of /

cat > "$expected_output" <<EOF
1
*
3
4
5
*
EOF

seq 1 6 | eddy.py 's_[26]_*_' > "$actual_output" 2>&1

#Check if output produced matches the output expected

if ! diff "$expected_output" "$actual_output"; then
    echo "test06-1: ${Red}Failed test${No_colour}"
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
    echo "test06-1: ${Green}Passed test${No_colour}"
    count=$((count+1))
fi

#-------------------------------------------------------------------------------------

#test06-2
#eddy s with X instead of /

cat > "$expected_output" <<EOF
11
1*
13
14
15
1*
EOF

seq 11 16 | eddy.py 'sX[26]X*X' > "$actual_output" 2>&1

#Check if output produced matches the output expected

if ! diff "$expected_output" "$actual_output"; then
    echo "test06-2: ${Red}Failed test${No_colour}"
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
    echo "test06-2: ${Green}Passed test${No_colour}"
    count=$((count+1))

fi

#-------------------------------------------------------------------------------------

#test06-3
#eddy s with : instead of /

cat > "$expected_output" <<EOF
*2
*3
*4
*5
EOF

seq 22 25 | eddy.py 's:[26]:*:' > "$actual_output" 2>&1

#Check if output produced matches the output expected

if ! diff "$expected_output" "$actual_output"; then
    echo "test06-3: ${Red}Failed test${No_colour}"
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
    echo "test06-3: ${Green}Passed test${No_colour}"
    count=$((count+1))
fi

if [ $count -eq 3 ]
then 
    exit 0
fi