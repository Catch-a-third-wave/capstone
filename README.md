# Capstone project: Catch a third wave
by Laura Dell' Antonio and Jakolien den Hollander

## About the project

Our stakeholder, the World Health Organisation (WHO) wants to get an insight into the world wide Covid-19 pandemic with a focus on the relationship between the number of COVID-19 cases and:
* Mask wearing
  * Mind that we have no mask data for the USA
* Social distancing
The WHO is hoping for our analysis to provide proof that mask-wearing and social distancing are effective means in reducing the number of COVID-19 cases world wide.

### Model 
Do the advised measures, staying at home and wearing masks, flatten the curve of COVID-cases? This is measured by comparing countries in which inhabitants adhere to these measures to countries in which these measures are not being adhered to.

### Additional goals
The WHO is interested in cultural and political impacts on social distancing measures.
* CULTURAL: impact of national preferred interpersonal distance on social distancing
* POLITICAL: impact of Trump’s tweets on social distancing in the US
  * If we cannot obtain the twitter data, another NLP component will be introduced.

## Deliverables
* Presentation to the WHO, especially to the COVID task force, on our findings on how mask-wearing and social distancing relate to the COVID numbers in various countries around the globe.
* Interactive map with a play button showing how the COVID cases develop as well as how mask-wearing and social distancing measurers change over the months.
  * If possible with a selection option (wearing masks/social distancing) showing how COVID numbers change in  countries in which mask wearing and social distancing are being practiced compared to where they are not.
* A model to predict the number of COVID cases based on mask-wearing and social distancing.
  * A SIR Model might be relevant to model future disease spread



# Create the capstone environment
Requires node to be installed (https://nodejs.org/en/)
```bash
conda create --name capstone python=3.8.5
conda install -n capstone pytest==6.1.1
conda install -n capstone ipython
conda install -n capstone jupyterlab
conda install -n capstone seaborn
conda install -n capstone scikit-learn
conda install -n capstone numpy
conda install -n capstone pandas
conda install -n capstone statsmodels
conda install -n capstone sklearn
conda install -n capstone nb_conda
conda install -n capstone xlrd
conda install -c plotly plotly=4.13.0
conda install jupyterlab "ipywidgets=7.5"
jupyter labextension install jupyterlab-plotly@4.13.0
jupyter labextension install @jupyter-widgets/jupyterlab-manager plotlywidget@4.13.0
conda install -c conda-forge dash
pip install tensorflow
pip install keras
```
