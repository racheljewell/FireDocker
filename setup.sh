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

    # mk dir for FireDocker and/or move it
    echo -e -n "\033[32mDefining the target directory: \033[0m"
    #mkdir /usr/local/bin/FireDocker
    cd ..
    TARGET_DIR="/usr/local/bin/"
    echo "$TARGET_DIR"


    # Move the entire FireDocker directory and its contents to the target directory
    echo -e "\033[32mMoving the FireDocker directory and its contents to the target directory ...\033[0m"
    cp -rp "FireDocker" "$TARGET_DIR/FireDocker"
    if [ $? -ne 0 ]; then
        echo -e "\033[31mERROR STATUS FAILED TO MOVE FireDocker DIRECTORY TO TARGET DIR CODE 2\033[0m"
       exit 1 
    fi


    # Change the execute permissions to make the script executable
    echo -e "\033[32mChanging permissions on script\033[0m"
    chmod +x "$TARGET_DIR/FireDocker/$SCRIPT_NAME"

    # Create a symbolic link in the user's bin directory for easy execution
    ln -s "$TARGET_DIR/FireDocker/$SCRIPT_NAME" "/usr/local/bin/firedocker"
    if [ $? -ne 0 ]; then
        echo -e "\033[31mERROR STATUS SYMBOLIC LINK FAILED CODE 3 \033[0m"
        exit 1
    fi
    echo -e "\033[32mScript setup complete. You can now execute 'firedocker' from anywhere.\033[0m"

   
else
    echo -e "\033[31mERROR STATUS NOT ROOT USER CODE 1...Please Run Again Using 'sudo' Or As Root User \033[0m"
fi

