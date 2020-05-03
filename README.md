<p align="center"><img width=75% alt="" src="app/static/img/manita.png"></a></p>

# manita

[![Build Status](https://travis-ci.com/zenoxygen/manita.svg?branch=master)](https://travis-ci.com/zenoxygen/manita)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

Mushroom identification using deep learning.

## About

Manita is a web application that helps to identify mushrooms from pictures.

1. Upload a mushroom image
2. Start the analysis process
3. Get more information about the prediction

## Installation

You can build, run and test locally by installing Docker and using the following command:

```
docker build -t manita . && docker run --rm -it -p 5000:5000 manita
```

## Training

You can train your own model on [Google Colab](https://colab.research.google.com) using the script provided in the `train` folder.

## Contribution

Your contribution will always be welcome.

## License

Manita is licensed under the [MIT License](LICENSE).
