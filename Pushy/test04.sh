#!/bin/dash

############################################################################################################
#
#                                       ASSIGNMENT 1 - COMP2041
#                                            TEST SCRIPT 04
#
#                                       by  Ayusha Priyadarshani
#                                               z5452643
#
#                                              23-03-2024
#                    
############################################################################################################
#Tests pushy-show features and errors 

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

echo "\tpushy-show"

#test04-1 
#Call pushy-show using incorrect syntax

cat > "$expected_output" <<EOF
usage: pushy-show <commit>:<filename>
EOF

pushy-show > "$actual_output" 2>&1

#Check if output produced matches the output expected

if ! diff "$expected_output" "$actual_output"; then
    echo "test04-1: ${Red}Failed test${No_colour}"
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
    echo "test04-1: ${Green}Passed test${No_colour}"
fi

#-------------------------------------------------------------------------------------

#test04-2 
#Call pushy-show before commit

cat > "$expected_output" <<EOF
pushy-show: error: unknown commit '0'
EOF

pushy-init >/dev/null
echo hey >file1 
echo hola >file2
pushy-add file1 file2
pushy-show 0:file2 > "$actual_output" 2>&1

#Check if output produced matches the output expected

if ! diff "$expected_output" "$actual_output"; then
    echo "test04-2: ${Red}Failed test${No_colour}"
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
    echo "test04-2: ${Green}Passed test${No_colour}"
fi

#-------------------------------------------------------------------------------------

#test04-3
#Call pushy-show with incorrect commit

cat > "$expected_output" <<EOF
pushy-show: error: unknown commit '1'
EOF

pushy-init >/dev/null
echo hey >file1 
echo hola >file2
pushy-add file1 file2
pushy-commit -m "first commit" >/dev/null
pushy-show 1:file1 > "$actual_output" 2>&1

#Check if output produced matches the output expected

if ! diff "$expected_output" "$actual_output"; then
    echo "test04-3: ${Red}Failed test${No_colour}"
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
    echo "test04-3: ${Green}Passed test${No_colour}"
fi

#-------------------------------------------------------------------------------------

#test04-4
#Call pushy-show with incorrect file

cat > "$expected_output" <<EOF
pushy-show: error: 'file3' not found in commit 0
EOF

pushy-init >/dev/null
echo hey >file1 
echo hola >file2 
pushy-add file1 file2 
pushy-commit -m "first commit" >/dev/null
pushy-show 0:file3 > "$actual_output" 2>&1

#Check if output produced matches the output expected

if ! diff "$expected_output" "$actual_output"; then
    echo "test04-4: ${Red}Failed test${No_colour}"
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
    echo "test04-4: ${Green}Passed test${No_colour}"
fi

#-------------------------------------------------------------------------------------

#test04-5
#Call pushy-show with correct arguments

cat > "$expected_output" <<EOF
hey
EOF

pushy-init >/dev/null
echo hey >file1 
echo hola >file2
pushy-add file1 file2 
pushy-commit -m "first commit" >/dev/null
echo there >>file1 
pushy-add file1 
pushy-commit -m "second commit" >/dev/null
pushy-show 0:file1 > "$actual_output" 2>&1

#Check if output produced matches the output expected

if ! diff "$expected_output" "$actual_output"; then
    echo "test04-5: ${Red}Failed test${No_colour}"
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
    echo "test04-5: ${Green}Passed test${No_colour}"
fi

#-------------------------------------------------------------------------------------

#test04-6
#Call pushy-show with only file name, no commit number
#File will be displayed from index

cat > "$expected_output" <<EOF
hey
there
EOF

pushy-init >/dev/null
echo hey >file1 
echo hola >file2
pushy-add file1 file2 
pushy-commit -m "first commit" >/dev/null
echo there >>file1 
pushy-add file1 
pushy-commit -m "second commit" >/dev/null
pushy-show :file1 > "$actual_output" 2>&1

#Check if output produced matches the output expected

if ! diff "$expected_output" "$actual_output"; then
    echo "test04-6: ${Red}Failed test${No_colour}"
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
    echo "test04-6: ${Green}Passed test${No_colour}"
fi
