if [ $1 ] 
then
    mkdir src
    cd src
    catkin_create_pkg $1
    cd ..
    catkin_make
else
    echo "Please pass the name of the package you want to create."
fi
