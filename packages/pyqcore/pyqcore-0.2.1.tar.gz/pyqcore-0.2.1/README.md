![Logo](./pics/logo.png)

--------------------------------------------------------------------------------

PyQCore is a client in Python to access our high speed reservoir computing engine, WebQore.  

We are in an early-release beta. Expect some adventures and rough edges.
  
### Update  
2019.06.13  Release 0.2.1:  Add `sofmax_top` option to `classification_predict` to show the softmax values with predicted classes.
2019.03.08  Release 0.2.0:  Add `regression_train`, `regression_test`, `regression_predict`.  

- [More about PyQCore](#more-about-pyqcore)
  - [About QuantumCore Engine](#about-quantumcore-engine)
- [Installation](#installation)
- [Getting Started](#getting-started)
- [Communication](#communication)
- [License](#license)



## More about PyQCore

At a granular level, PyQcore is a library that consists of the following components:

| Component                             | Description                                                                                                                                   |
| ------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| **pyqcore.client.SimpleQCoreClient**  | a client class that makes model on WebQore Engine                                                                                             |
| **pyqcore.examples.jpvow.load_jpvow** | a function that loads sample data from [UCI repository](https://archive.ics.uci.edu/ml/datasets/Japanese+Vowels) and return as sklearn format |

This library is enable to use the WebQore Engine in your codes. Also you need get license code from QuantumCore website to use this library([QuantumCore Inc.](https://www.qcore.co.jp) ).

### About QuantumCore Engine

WebQore Engine is developed by [QuantumCore Inc.](https://www.qcore.co.jp) This new model is 4Kx faster and lighter than previous LSTM or RNN model without GPU. Also you do not have to adjust parameters anymore.  
The Engine you use with this library is currently running on t2.micro on AWS ([check out the speck here](https://aws.amazon.com/ec2/instance-types/)).  
 The company also plans to impliment this algorithm on small edge computer.



## Installation  
This library requires **Python > 3.5**.  

Installing PyQcore is not difficult. Just run the command below:

```
pip install pyqcore
```
Or clone this repository and run:

```
python setup.py install
```


## Getting Started

Refer our [sample scrpts](./docs/sample.py) or [tutorial notebook](./docs/tutorial1.ipynb).  
Make sure that you need get license code from [QuantumCore Inc.](https://www.qcore.co.jp)

## Communication
* GitHub issues: bug reports, feature requests, install issues, RFCs, thoughts, etc.
* Mailing List: please send any issue at [info-dev@qcore.co.jp](mailto:info-dev@qcore.co.jp)


## License

Copyright (c) 2019 QuantumCore Inc.

