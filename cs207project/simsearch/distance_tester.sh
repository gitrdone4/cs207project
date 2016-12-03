echo "This script checks the distance of a new time series against a database. Please enter the file name of the new time series"
echo "Please make sure that the time series file is correctly formatted"
read filename
python Distance_from_known_ts.py $filename
