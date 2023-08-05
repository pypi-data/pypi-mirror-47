# hands_rdf

Library with utils to segment hands onto RGBD images.
The library is used in [hands_cv project](https://github.com/BernatGalmes/hands_cv).

Note that the software architecture goes around the Model.Config class.
In this class we should specify:
* The path of the dataset we are using.
* The number of features to use.
* And all the parameters that we want to use in our classifier.


## Functionality
The library is composed by Two main classes:

### Features class
Class used to compute the features used by our classifier.

### RDF class
Class that define the classifier used to segment hands.

### Helpers functions
The helpers functions are all complementary functions used by the library.


## Model module
That module contain all the code used to manage the data used by the library.
It contains a Config class that define all the parameters and constants
used by the library.
It also contain all the code used to manage the dataset.


### Train and test models
Basically, outside the library the unique useful classes are
TrainModels and TestModels.

Those libraries are used to build the train and the test datasets.

## Configure library
Before using the library you should configure some parameters in class
Model.Config.

* Config.FOLDER_DATASETS: This parameter should specify
the path of the datasets.
* Config.DATASET: Specify the name of the folder of the dataset
that you want to use (inside Config.FOLDER_DATASETS folder).


## Example of usages

### Creating the RDF

Next shows how to create an RDF:
```python
from hands_rdf.RDF import RDF
clf = RDF()
```

### Generate Features

Next shows how to create an RDF:
```python
from hands_rdf.features import Features
f = Features()
```

### Get the probability of pixels to be hand

Next we illustrate an example of how the get the probability of each pixel to be a hand.

First step is with a depth map and the constant value of the background, get
all the positions that should belong to a hand.
```python
indexs = np.nonzero(depth_image < bg_value)
```

Once we have those positions we get the value of all the features of those pixels.
```python
positions, features = f.get_image_features(depth_image, indexs)
```

Using that set of features we can get the probability of belonging to a
hand for each pixel. In this example we use that prediction to build an image
(proba_mask) that shows the results graphically.
```python
proba_mask = np.zeros((depth_image.shape[0], depth_image.shape[1]),
                          dtype=np.float32)
predicted = clf.predict_proba(features)
proba_mask[positions] = predicted[:, 1]
```

### Extra details
Extra project details can be found [Here](https://bernatgalmes.github.io/hands_rdf/docs/results.html).