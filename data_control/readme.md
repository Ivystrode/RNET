## Data stuff

- Collect data (acquire imagesets, scan reports)
- Use imagesets to train detection models
- Sort scan reports for device tracking

Be Aware - need to make a permanent solution for data_db's path in the dbcon file. When called from other modules it will need the whole path ie from the project root

Datasets are ignored by git for obvious reasons!!

Model creation (single class classification):
- Split data between train and test directories, inside subject directory (as usual)
- Binary classification - for single object detection/classification we therefore also need to add a "0" class to represent "not detected/present"
- Do this by creating two sub-dirs in the train & test dirs. These are read ***in alphanumeric order*** - so the first folder will be class "0"
- Need to add a dataset of random images to the train and test folders (try use equal number of random images as of the actual dataset, auto-downloader.py currently uses https://picsum.photos/200/200/?random)
- Use stochastic gradient descent optimizer
- add shuffle = true to generalize better