#!/bin/dash

############################################################################################################
#
#                                       ASSIGNMENT 1 - COMP2041
#                                            TEST SCRIPT 05
#
#                                       by  Ayusha Priyadarshani
#                                               z5452643
#
#                                              23-03-2024
#                    
############################################################################################################
#Tests pushy-commit -a -m features and errors 

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

#-------------------------------------------------------------------------------------

echo "  pushy-commit -a -m"

#test05-1 
#Call pushy-commit using incorrect syntax

cat > "$expected_output" <<EOF
usage: pushy-commit [-a] -m commit-message
EOF

pushy-init >/dev/null
echo "g'day" >file 
pushy-commit -a > "$actual_output" 2>&1

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
fi

#-------------------------------------------------------------------------------------

#test05-2
#Call pushy-commit using correct syntax

cat > "$expected_output" <<EOF
g'day
mate
EOF

pushy-init >/dev/null
echo "g'day" >file 
pushy-add file
echo mate >>file
pushy-commit -a -m "added file" >/dev/null
pushy-show 0:file > "$actual_output" 2>&1

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
fi
