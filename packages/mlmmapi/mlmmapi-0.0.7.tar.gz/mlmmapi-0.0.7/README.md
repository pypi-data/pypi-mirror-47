# interaction-grader
Python package to help grade test questions (interactions) using trained machine learning models.

The Answer class can be used to check if an answer is basically identical to the desired answer except 
for misspellings.

Initial version hard codes a model already trained to recognize actor names from a list of 322.
  
```Python
# Example usage
from mlmmapi import check_answer

correct_answer = 'Joaquim Phoenix'
answer = 'Joakim Pheonix'
correct, prediction, score = check_answer(answer, correct_answer)  
if correct:  
    print('Correct Answer')
else:    
    print('Prediction: {} - score: {}'.format(prediction, score))  
```

- Package Dependencies:  
    * fuzzywuzzy  
    * python-Levenshtein  
    * numpy
    * pandas
    * sklearn
    * xgboost
    * joblib  


Build Package:

1. Setup a virtual environment 
    * Insure you have python3.x instaled
    * python3 -m venv env
    * source env/bin/activate
2. Install all packages listed in the dependencies
    * pip3 install <...>
3. pip3 install .
4. Test the code above in the example in python3
5. Check pypi.org for the lastest version of the mlmmapi package
    * update the setup.py to have the next version number to push to pypi
    * Commit the latest setup.py to the repo
6. Build the package
    * python3 setup.py sdist
7. Upload the package
8. Install the twine package
    * pip3 install twine
9. Upload the package
    * twine upload dist/*            

    