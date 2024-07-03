#!/bin/dash

############################################################################################################
#
#                                       ASSIGNMENT 2 - COMP2041
#                                            TEST SCRIPT 04
#                                               SUBSET 0
#
#                                       by  Ayusha Priyadarshani
#                                               z5452643
#
#                                              22-04-2024
#                    
############################################################################################################
#Tests eddy s features and errors 

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

echo "\teddy s"

#test04-1 
#Call eddy s with []

cat > "$expected_output" <<EOF
5
6
7
8
<
10
11
EOF

seq 5 11 | eddy.py 's/9/</' > "$actual_output" 2>&1

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
    count=$((count+1))
fi

#-------------------------------------------------------------------------------------

#test04-2 
#Call eddy s with [ ]

cat > "$expected_output" <<EOF
9
ok0
ok1
ok2
ok3
ok4
ok5
EOF

seq 9 15 | eddy.py 's/[17]/ok/' > "$actual_output" 2>&1

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
    count=$((count+1))
fi

#-------------------------------------------------------------------------------------

#test04-3
#Call eddy s with pattern

cat > "$expected_output" <<EOF
199
<00
201
202
203
204
EOF

seq 199 204 | eddy.py '2s/2/</' > "$actual_output" 2>&1

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
    count=$((count+1))
fi

#-------------------------------------------------------------------------------------

#test04-4
#Call eddy s with pattern, repeated replacement allowed (g)

cat > "$expected_output" <<EOF
201
<0<
203
204
EOF

seq 201 204 | eddy.py '2s/2/</g' > "$actual_output" 2>&1

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
    count=$((count+1))
fi

#-------------------------------------------------------------------------------------

#test04-5
#Call eddy s with words

cat > "$expected_output" <<EOF
hola amigos!
EOF

echo holaa amigos! | eddy.py 's/a//' > "$actual_output" 2>&1

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
    count=$((count+1))
fi

#-------------------------------------------------------------------------------------

#test04-6
#Call pushy-show with only file name, no commit number
#File will be displayed from index

cat > "$expected_output" <<EOF
hol migos!
EOF

echo holaa amigos! | eddy.py 's/a//g' > "$actual_output" 2>&1

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
    count=$((count+1))
fi

if [ $count -eq 6 ]
then 
    exit 0
fi