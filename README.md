# blackbox-trading-CNN
Time Series Classification with Convolutional Neural Network: Automated Trading by Pattern Recognition (Master's Thesis)

## Prequisites
All parts are written in Python 3 (except report which is in LaTex) the requirements can be installed using:

```
pip install -r requirements.txt

```
For the CNN and Data preparation I used Jupyter notebooks.

## Content

### data
All downloaded datasets, trial code for data retrivals via API.
**/data_raw/\*** has all raw datasets used to create the inputs

 **/cnn_input/\*** has all folders that will hold all inputs for the CNN given the *data-check-and-prep-alldata-2Y.ipynb* notebook is ran.

**/competing-strategies-signals/\*** contains the signals for the test assets based on the RSI and BB algorithmic trading trading_strategies

**/logs/\*** gets all logs from *data-check-and-prep-alldata-2Y.ipynb*

### notebooks
Jupyter notebooks of CNN versions and Data Preparation

* **data-check-and-prep-alldata-2Y** uses prewritten modules (See utils) to preliminarily check/modify the data, label and transform it to be ready for the CNN. It visualizes the input/output data and labelling. Its input is any raw dataset (**data/data_raw**), its output goes into data/cnn_input/ and serves as input for the CNN notebooks.

* **Google Colab codes/\*** holds all asset-specific and universal model codes which are trained and tested in 3 different training periods (dates for period 2 to be checked in notebooks that are not ran on period two in case of general use.) CNN, Keras

* **financial-evaluation** takes all results from the **Results** folder and **competing-strategies-signals** folder and  returns financial performance measurements and figures

* **competing-strategies** creates trading signals for the same datasets given RSI and BB algorithmic trading strategy

* **classification&time-evaluation** takes all results from the **Results** folder and returns classification performance metrics

* **/Output/** contains logs from the CNN, later will contain other evaluation outputs as well

### results tables
Contains all result outputs from *financial-evaluation.ipynb** and *classification&time-evaluation.ipynb*, contains general results table

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
