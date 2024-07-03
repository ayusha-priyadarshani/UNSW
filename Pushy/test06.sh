#!/bin/dash

############################################################################################################
#
#                                       ASSIGNMENT 1 - COMP2041
#                                            TEST SCRIPT 06
#
#                                       by  Ayusha Priyadarshani
#                                               z5452643
#
#                                              24-03-2024
#                    
############################################################################################################
#Tests pushy-rm features and errors 

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

echo "\tpushy-rm"

#test06-1 
#Call pushy-rm without any arguments

cat > "$expected_output" <<EOF
usage: pushy-rm [--force] [--cached] <filenames>
EOF

pushy-init >/dev/null
pushy-rm > "$actual_output" 2>&1

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
fi

#-------------------------------------------------------------------------------------

#test06-2
#pushy-rm file - safe removal

cat > "$expected_output" <<EOF
a - file deleted, deleted from index
EOF

pushy-init >/dev/null
echo hi >a
pushy-add a
pushy-commit -m "first" >/dev/null
pushy-rm a 
pushy-status > "$actual_output" 2>&1

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
fi

#-------------------------------------------------------------------------------------

#test06-3
#pushy-rm file - unsafe removal

cat > "$expected_output" <<EOF
pushy-rm: error: 'a' has staged changes in the index
EOF

pushy-init >/dev/null
echo hi >a
pushy-add a
pushy-commit -m "first" >/dev/null
echo hey >>a
pushy-add a
pushy-rm a > "$actual_output" 2>&1

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
fi

#-------------------------------------------------------------------------------------

#test06-4
#pushy-rm file - only index removal

cat > "$expected_output" <<EOF
a - deleted from index
EOF

pushy-init >/dev/null
echo hi >a
pushy-add a
pushy-commit -m "first" >/dev/null
pushy-rm --cached a 
pushy-status > "$actual_output" 2>&1

#Check if output produced matches the output expected

if ! diff "$expected_output" "$actual_output"; then
    echo "test06-4: ${Red}Failed test${No_colour}"
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
    echo "test06-4: ${Green}Passed test${No_colour}"
fi

#-------------------------------------------------------------------------------------

#test06-5
#pushy-rm file - forced removal before commit but same file present in repository

cat > "$expected_output" <<EOF
a - file deleted, deleted from index
EOF

pushy-init >/dev/null
echo hi >a
pushy-add a
pushy-commit -m "first" >/dev/null
pushy-rm a
echo hi >a
pushy-add a
pushy-rm --force a 
pushy-status > "$actual_output" 2>&1

#Check if output produced matches the output expected

if ! diff "$expected_output" "$actual_output"; then
    echo "test06-5: ${Red}Failed test${No_colour}"
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
    echo "test06-5: ${Green}Passed test${No_colour}"
fi

#-------------------------------------------------------------------------------------

#test06-5
#pushy-rm file - forced removal before commit but different file present in repository

cat > "$expected_output" <<EOF
EOF

pushy-init >/dev/null
echo hi >a
pushy-add a
pushy-commit -m "first" >/dev/null
pushy-rm a
echo hey >a
pushy-add a
pushy-rm --force a 
pushy-status > "$actual_output" 2>&1

#Check if output produced matches the output expected

if ! diff "$expected_output" "$actual_output"; then
    echo "test06-6: ${Red}Failed test${No_colour}"
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
    echo "test06-6: ${Green}Passed test${No_colour}"
fi