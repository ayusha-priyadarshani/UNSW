#!/bin/dash

############################################################################################################
#
#                                       ASSIGNMENT 1 - COMP2041
#                                            TEST SCRIPT 01
#
#                                       by  Ayusha Priyadarshani
#                                               z5452643
#
#                                              21-03-2024
#                    
############################################################################################################
#Tests pushy-add features and errors 

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

echo "\tpushy-add"

#test01-1 
#Call pushy-add before pushy-init

cat > "$expected_output" <<EOF
pushy-add: error: pushy repository directory .pushy not found
EOF

pushy-add > "$actual_output" 2>&1

#Check if output produced matches the output expected

if ! diff "$expected_output" "$actual_output"; then
    echo "test01-1: ${Red}Failed test${No_colour}"
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
    echo "test01-1: ${Green}Passed test${No_colour}"
fi

#-------------------------------------------------------------------------------------

#test01-2
#Call pushy-add after pushy-init, without specifying file

cat > "$expected_output" <<EOF
usage: pushy-add <filenames>
EOF

#Storing pushy-init output in Null
pushy-init >/dev/null 

pushy-add > "$actual_output" 2>&1

#Check if output produced matches the output expected

if ! diff "$expected_output" "$actual_output"; then
    echo "test01-2: ${Red}Failed test${No_colour}"
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
    echo "test01-2: ${Green}Passed test${No_colour}"
fi

#-------------------------------------------------------------------------------------

#test01-3
#Call pushy-add after pushy-init, specify incorrect file

cat > "$expected_output" <<EOF
pushy-add: error: can not open 'b'
EOF

#Storing pushy-init output in Null
pushy-init >/dev/null 

echo hi >a 

pushy-add b > "$actual_output" 2>&1

#Check if output produced matches the output expected

if ! diff "$expected_output" "$actual_output"; then
    echo "test01-3: ${Red}Failed test${No_colour}"
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
    echo "test01-3: ${Green}Passed test${No_colour}"
fi

#-------------------------------------------------------------------------------------

#test01-4
#Call pushy-add after pushy-init, specify correct file

cat > "$expected_output" <<EOF
EOF

#Storing pushy-init output in Null
pushy-init >/dev/null 

echo hi >a 

pushy-add a > "$actual_output" 2>&1

#Check if output produced matches the output expected

if ! diff "$expected_output" "$actual_output"; then
    echo "test01-4: ${Red}Failed test${No_colour}"
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
    echo "test01-4: ${Green}Passed test${No_colour}"
fi