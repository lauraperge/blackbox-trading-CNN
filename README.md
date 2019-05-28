# blackbox-trading-CNN
Time Series Classification with Convolutional Neural Network: Automated Trading by Pattern Recognition (Master's Thesis)

blackbox-trading-CNN
Time Series Classification with Convolutional Neural Network: Automated Trading by Pattern Recognition (Master's Thesis)

## Getting Started
TBD

## Prequisites
All parts are written in Python 3 (except report which is in LaTex) the requirements can be installed using:

```
pip install -r requirements.txt

```
For the CNN and Data preparation I used Jupyter notebooks.

## Content

### data
All downloaded datasets, trial code for data retrivals via API.

* **gemini_BTCUSD 1 minute data\*** (2015-2019) Retrieved: 02-03-2019 https://www.CryptoDataDownload.com

* **IVE_bidask1min_iShares S&P 500 Value Index.csv** (2009-2019) Retrieved: 2019-03-02 http://api.kibot.com

* **/cnn_input/\*** has all datasets containing the series, labels and image representations for the CNN

### notebooks
Jupyter notebooks of CNN versions and Data Preparation

* **data-check-and-prep** uses prewritten modules (See utils) to preliminarily check/modify the data, label and transform it to be ready for the CNN. It visualizes the input/output data and labelling. Its input is any raw dataset from the data or via API, its output goes into data/cnn_input/ and serves as input for the CNN notebooks.

* **CNN-trial-version** is the first working version of a tensorflow CNN model with a test dataset and single color channel. It is not optimized or enhanced. input data is the output of data-check-and-prep

* **CNN-trial-version-multiple color channels** is the first working version of a tensorflow CNN model with a test dataset and multiple color channels. It is not optimized or enhanced. input data is the output of data-check-and-prep

* **/Output/** contains logs from the CNN, later will contain other evaluation outputs as well

### report
LaTeX report

### utils
All custom modules for obtaining, examining, preparing, cleaning, labelling, and transforming data into images, as well as a code to prepare input for the tensorflow CNN

* **data cleaning**: read in raw data, turn into pandas time series, resampling if needed, missing value checks, reporting feature

* **get_data**: functions to retrieve historical cryptocurrency data, stock prices and fx prices via API connections (sources: bitfinex, yahoo, fred)

* **labelled_image_preparation**: takes vector as input, returns the transformed version as images of given size according to given transformation strategy/strategies with relevant trading labels that serves as an input for the tensorflow CNN

#### labels
labelling strategy for the time series

* **trading_strategies**: local min-max implementation

#### transform
* **gramian angular field**: for creating one ore more gramain angular summation/difference fields from a vector representing a series of observations

* **markov_transition_field**: for creating one or more markov transition fields from a vector representing a series of observations (as per https://www.researchgate.net/publication/275970614_Encoding_Time_Series_as_Images_for_Visual_Inspection_and_Classification_Using_Tiled_Convolutional_Neural_Networks)

* **recurrence_plot**: for creating one or more recurrence plots from a vector representing a series of observations (as per https://arxiv.org/abs/1710.00886)

#### visualize
* **ts_with_markers**: show trading strategy Buy/Sell points on time series
