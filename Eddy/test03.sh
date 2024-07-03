#!/bin/dash

############################################################################################################
#
#                                       ASSIGNMENT 2 - COMP2041
#                                            TEST SCRIPT 03
#                                               SUBSET 0
#
#                                       by  Ayusha Priyadarshani
#                                               z5452643
#
#                                              22-04-2024
#                    
############################################################################################################
#Tests eddy d features and errors 

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

echo "\teddy d"

#test03-1 
#Call eddy d without number
cat > "$expected_output" <<EOF
EOF

seq 1 5 | eddy.py d > "$actual_output" 2>&1

#Check if output produced matches the output expected

if ! diff "$expected_output" "$actual_output"; then
    echo "test03-1: ${Red}Failed test${No_colour}"
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
    echo "test03-1: ${Green}Passed test${No_colour}"
    count=$((count+1))
fi

#-------------------------------------------------------------------------------------

#test03-2
#Call eddy d with number

cat > "$expected_output" <<EOF
1
2
3
5
EOF

seq 1 5 | eddy.py 4d > "$actual_output" 2>&1

#Check if output produced matches the output expected

if ! diff "$expected_output" "$actual_output"; then
    echo "test03-2: ${Red}Failed test${No_colour}"
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
    echo "test03-2: ${Green}Passed test${No_colour}"
    count=$((count+1))
fi

#-------------------------------------------------------------------------------------

#test03-3
#Call eddy d with regex

cat > "$expected_output" <<EOF
31
33
35
37
EOF

seq 31 38 | eddy.py '/[2468]/d' > "$actual_output" 2>&1

#Check if output produced matches the output expected

if ! diff "$expected_output" "$actual_output"; then
    echo "test03-3: ${Red}Failed test${No_colour}"
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
    echo "test03-3: ${Green}Passed test${No_colour}"
    count=$((count+1))
fi

#-------------------------------------------------------------------------------------

#test03-4
#Call eddy d with range

cat > "$expected_output" <<EOF
1
2
3
7
8
9
EOF

seq 1 9 | eddy.py '/4/,/6/d' > "$actual_output" 2>&1

#Check if output produced matches the output expected

if ! diff "$expected_output" "$actual_output"; then
    echo "test03-4: ${Red}Failed test${No_colour}"
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
    echo "test03-4: ${Green}Passed test${No_colour}"
    count=$((count+1))
fi

#-------------------------------------------------------------------------------------

#test03-5
#Call eddy $d 

cat > "$expected_output" <<EOF
32
33
34
35
36
EOF

seq 32 37 | eddy.py '$d' > "$actual_output" 2>&1

#Check if output produced matches the output expected

if ! diff "$expected_output" "$actual_output"; then
    echo "test03-5: ${Red}Failed test${No_colour}"
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
    echo "test03-5: ${Green}Passed test${No_colour}"
    count=$((count+1))
fi

if [ $count -eq 5 ]
then 
    exit 0
fi