#!/bin/dash

############################################################################################################
#
#                                       ASSIGNMENT 1 - COMP2041
#                                            TEST SCRIPT 03
#
#                                       by  Ayusha Priyadarshani
#                                               z5452643
#
#                                              23-03-2024
#                    
############################################################################################################
#Tests pushy-log features and errors 

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

echo "\tpushy-log"

#test03-1 
#Call pushy-log without initializing repository

cat > "$expected_output" <<EOF
pushy-commit: error: pushy repository directory .pushy not found
EOF

pushy-log > "$actual_output" 2>&1

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
fi

#-------------------------------------------------------------------------------------

#test03-2
#Call pushy-log after initializing repository

cat > "$expected_output" <<EOF
EOF

pushy-init >/dev/null
pushy-log > "$actual_output" 2>&1

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
fi

#-------------------------------------------------------------------------------------

#test03-3
#Call pushy-log after adding file to index but before commiting

cat > "$expected_output" <<EOF
EOF

pushy-init >/dev/null
echo "g'day" >file 
pushy-add file 
pushy-log > "$actual_output" 2>&1

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
fi

#-------------------------------------------------------------------------------------

#test03-4
#Call pushy-log after commiting

cat > "$expected_output" <<EOF
0 first commit
EOF

pushy-init >/dev/null
echo "g'day" >file 
pushy-add file 
pushy-commit -m "first commit" >/dev/null
pushy-log > "$actual_output" 2>&1

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
fi

#-------------------------------------------------------------------------------------

#test03-5
#Call pushy-log after multiple commits

cat > "$expected_output" <<EOF
1 second commit
0 first commit
EOF

pushy-init >/dev/null
echo "g'day" >file 
pushy-add file 
pushy-commit -m "first commit" >/dev/null
echo "mate" >>file
echo "namaste" >doc 
pushy-add file doc 
pushy-commit -m "second commit" >/dev/null
pushy-log > "$actual_output" 2>&1

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
fi