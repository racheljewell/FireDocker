#!/bin/bash
# ERROR CODES
# 0
# 1 NOT ROOT USER
# 2 MV FILE TO TARGET DIR FAILED 
# 3 SYMBOLIC LINK FAILED

if pgrep -s 0 "^sudo$" > /dev/null ; then
    echo -e "\033[32mI am  $USER\033[0m"

    echo -e -n "\033[32mDefining name of python script: \033[0m"
    SCRIPT_NAME="secdocker2.py"
    echo "$SCRIPT_NAME"

    echo -e -n "\033[32mDefining the target directory: \033[0m"
    TARGET_DIR="/usr/local/bin"
    echo "$TARGET_DIR"

    echo -e "\033[32mMoving the Python script to the target directory and creating a copy ...\033[0m"
    cp "$SCRIPT_NAME" "copy_secdocker2.py"
    mv "$SCRIPT_NAME" "$TARGET_DIR"
    if [ $? -ne 0 ]; then
        echo -e "\033[31mERROR STATUS FAILED TO MOVE FILE TO TARGET DIR CODE 2\033[0m"
       exit 1 
    fi

    # Change the execute permissions to make the script executable
    echo -e "\033[32mChanging permissions on script\033[0m"
    chmod +x "$TARGET_DIR/$SCRIPT_NAME"

    # Create a symbolic link in the user's bin directory for easy execution
    ln -s "$TARGET_DIR/$SCRIPT_NAME" "/usr/local/bin/secdocker2"
    if [ $? -ne 0 ]; then
        echo -e "\033[31mERROR STATUS SYMBOLIC LINK FAILED CODE 3 \033[0m"
        exit 1
    fi
    echo -e "\033[32mScript setup complete. You can now execute 'secdocker2' from anywhere.\033[0m"

else
    echo -e "\033[31mERROR STATUS NOT ROOT USER CODE 1...Please Run Again Using 'sudo' Or As Root User \033[0m"
fi
