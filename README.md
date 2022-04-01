# ml-association-rule
This project demonstrates the use of association rule, an unsupervised learning method. The association rule algorithm is integrated in a web app and performs Market Basket Analysis on a dataset of grocery transactions. This project was done primarily in Python but also uses Jupyter Notebook. A deployed demo of this app can be found under the [Deployed Demo](#demo) section.

## General Info
- Web App
  - File Info
    - [app.py](https://github.com/Evan-Lehmann/ml-association-rule/blob/main/app.py) compiles the individual pages into a multipage web app.
    - [multipage.py](https://github.com/Evan-Lehmann/ml-association-rule/blob/main/multipage.py) acts as a framework that allows multipage web apps.
    - [app_pages](https://github.com/Evan-Lehmann/ml-association-rule/tree/main/app_pages) contains the different pages of the web app.
    - [model.py](https://github.com/Evan-Lehmann/ml-association-rule/blob/main/app_pages/model.py) 
      - Contains the model itself and the original dataset.
        - The parameters can be altered. See [Algorithm](#algorithm) for more information on the algorithm and its parameters and see [Usage](#usage) for information on how to actually use the model.
        - Once the paramters are entered, a dataset will be generated revealing the association rules (or itemsets depending on metric used).
    - [dashboard.py](https://github.com/Evan-Lehmann/ml-association-rule/blob/main/app_pages/dashboard.py)
      - Dashboard with descriptive charts and statistics from the data.  
- Jupyter  Notebook
  - The Jupyter Notebook, [ml_association_rule.ipynb](https://github.com/Evan-Lehmann/ml-association-rule/blob/main/ml_association_rule.ipynb), serves primarily for exploratory purposes and does not affect the web app.

## <a name="algorithm">Algorithm</a>
- The association rule algorithm used is Apriori, see [here](http://rasbt.github.io/mlxtend/user_guide/frequent_patterns/association_rules/#association-rules-generation-from-frequent-itemsets) for full documentation on the algorithm.
  - Association Rules:
    - The algorithm returns association rules, which are given in pairs (antecedent and consequent).
    - Association Rules show relationships between data items and are in an if-then format.
  - Paramters (A = antecedent, C = consequent):
    - Support - frequency of itemsets in data, finds frequent itemsets, NOT association rules, value ranges from 0 to 1
      - Antecedent Support - same logic, but applies only to antecedent
      - Consequent Support - same logic, but applies only to consequent   
    - Confidence - conditional probability (how likely consequent is to be purchased when antecedent is purchased), value ranges from 0  to 1
    - Lift - measure how much more often the A and C of a rule occur together than we'd expect if they were independent, value ranges 
      from 0 to ∞
    - Leverage - difference between the observed frequency of A and C appearing together and expected frequency if A and C were 
      independent, value ranges from -1 to 1
    - Conviction - measure showing C's dependence on A, value ranges from 0 to ∞
   
## <a name="usage">Usage</a>
- [app.py](https://github.com/Evan-Lehmann/ml-association-rule/blob/main/app.py)
  - The web app can be launched locally by entering: 
    ```
    $ streamlit run app.py
    ```
- [model.py](https://github.com/Evan-Lehmann/ml-association-rule/blob/main/app_pages/model.py)
  - The first box, labeled, "Itemset Minimum Support", allows you to enter a support value threshold to find high frequency itemsets. 
    The association rules     
    will be generated from this itemset.
  - The second box, labeled "Rules Metric Type", allows you to choose the metric for the algorithm. If you choose any of the support  
    types, only itemsets will be generated, and not association rules.
  - The last box, labeled "Minimum {metric_type} value", allows you to enter a minimum threshold for the above metric, which will be   
    used to generate the association rules or itemsets.

## Dependencies
- Python Version:
 ```
 Python 3.10.1
 ```
- Python Packages:
 ```
 $ pip install -r requirements.txt
 ```
 
 ## <a name="demo">Deployed Demo</a>
 - A deployed demonstration of this app can be found at https://ml-association-rule-app.herokuapp.com/. The app was hosted using Heroku, a cloud platform used to work with applications. 
 - Deployment Dependencies 
    - [Procfile](https://github.com/Evan-Lehmann/ml-association-rule/blob/main/Procfile) is used to declare the commands run by the application's dynos. 
    - [setup.sh](https://github.com/Evan-Lehmann/ml-association-rule/blob/main/setup.sh) is used to add shell commands.
    - [.slugignore](https://github.com/Evan-Lehmann/ml-association-rule/blob/main/.slugignore) is used to remove files after code is pushed to Heroku.
    - [runtime.txt](https://github.com/Evan-Lehmann/ml-association-rule/blob/main/runtime.txt) is used to declare the Python version used.      

## License
This project is licensed under the [MIT license](LICENSE).

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
