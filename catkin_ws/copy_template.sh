if [ $1 -a $2 -a $3 ] 
then
  if [ $2 = "pub" ]
  then
    cp /home/jeff/rostools/pubtemplate.cpp src/$1
    mv src/$1/pubtemplate.cpp src/$1/$3
  fi
  if [ $2 = "sub" ]
  then
    cp /home/jeff/rostools/subtemplate.cpp $1
    mv $1/subtemplate.cpp $1/$3
  fi
else
  echo "You must pass 3 parameters: directory, pub/sub, and node name"
fi
