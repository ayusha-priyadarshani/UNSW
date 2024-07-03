#!/bin/dash

############################################################################################################
#
#                                       ASSIGNMENT 1 - COMP2041
#                                            TEST SCRIPT 02
#
#                                       by  Ayusha Priyadarshani
#                                               z5452643
#
#                                              22-03-2024
#                    
############################################################################################################
#Tests pushy-commit -m features and errors 

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

echo "\tpushy-commit"

#test02-1 
#Call pushy-commit without initializing repository

cat > "$expected_output" <<EOF
pushy-commit: error: pushy repository directory .pushy not found
EOF

pushy-commit > "$actual_output" 2>&1

#Check if output produced matches the output expected

if ! diff "$expected_output" "$actual_output"; then
    echo "test02-1: ${Red}Failed test${No_colour}"
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
    echo "test02-1: ${Green}Passed test${No_colour}"
fi

#-------------------------------------------------------------------------------------

#test02-2
#Initialize repository but call pushy-commit without -m

cat > "$expected_output" <<EOF
usage: pushy-commit [-a] -m commit-message
EOF

pushy-init >/dev/null
pushy-commit > "$actual_output" 2>&1

#Check if output produced matches the output expected

if ! diff "$expected_output" "$actual_output"; then
    echo "test02-2: ${Red}Failed test${No_colour}"
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
    echo "test02-2: ${Green}Passed test${No_colour}"
fi

#-------------------------------------------------------------------------------------

#test02-3
#Call pushy-commit -l <message>

cat > "$expected_output" <<EOF
usage: pushy-commit [-a] -m commit-message
EOF

pushy-init >/dev/null
pushy-commit -l haha > "$actual_output" 2>&1

#Check if output produced matches the output expected

if ! diff "$expected_output" "$actual_output"; then
    echo "test02-3: ${Red}Failed test${No_colour}"
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
    echo "test02-3: ${Green}Passed test${No_colour}"
fi

#-------------------------------------------------------------------------------------

#test02-4
#Call pushy-commit -m <message> without pushy-add

cat > "$expected_output" <<EOF
nothing to commit
EOF

pushy-init >/dev/null
pushy-commit -m haha > "$actual_output" 2>&1

#Check if output produced matches the output expected

if ! diff "$expected_output" "$actual_output"; then
    echo "test02-4: ${Red}Failed test${No_colour}"
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
    echo "test02-4: ${Green}Passed test${No_colour}"
fi

#-------------------------------------------------------------------------------------

#test02-5
#Call pushy-commit -m <message> with pushy-add

cat > "$expected_output" <<EOF
Committed as commit 0
EOF

pushy-init >/dev/null
echo hi! >file 
pushy-add file 
pushy-commit -m "first commit" > "$actual_output" 2>&1

#Check if output produced matches the output expected

if ! diff "$expected_output" "$actual_output"; then
    echo "test02-5: ${Red}Failed test${No_colour}"
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
    echo "test02-5: ${Green}Passed test${No_colour}"
fi

#-------------------------------------------------------------------------------------

#test02-6
#Call pushy-commit -m <message> twice, without changing index

cat > "$expected_output" <<EOF
nothing to commit
EOF

pushy-init >/dev/null
echo hi! >file 
pushy-add file 
pushy-commit -m "first commit" >/dev/null
pushy-commit -m "second commit" > "$actual_output" 2>&1

#Check if output produced matches the output expected

if ! diff "$expected_output" "$actual_output"; then
    echo "test02-6: ${Red}Failed test${No_colour}"
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
    echo "test02-6: ${Green}Passed test${No_colour}"
fi