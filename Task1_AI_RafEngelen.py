# %% [markdown]
# ## Task1: Cryptarithmetic puzzle 

# %% [markdown]
# ## Introduction
# In this file you will find some code written in comments. This is code that is only necessary to run on Streamlit. The version on Streamlit will have that code not in comments. I will explain the program step by step, I have created functions that will be called in the same order as you see in this file. These functions will be called in the main function.
# ## Imports and input
# First we need to import al necessary modules and ask for a puzzle.

# %%
from simpleai.search import CspProblem, backtrack
import re
import streamlit as st

# puzzle = input("Give a cryptarithmetic puzzle. ")
st.header('Raf Engelen - r0901812 - 3APP01', divider='gray')
st.title("Task 1 AI: Cryptarithmetic puzzle")
puzzle = st.text_input(
    label="Give a cryptarithmetic puzzle.", 
    placeholder="AI + IS = FUN", 
    label_visibility="visible")

# %% [markdown]
# ### Validating the input 
# We have gotten a string, but it might not be in a correct form (... + ... = ...). We will have check if the string is usable. The input needs has the following validation rules:
# 1. There is an operator (+, -, * or /)
# 2. There is an = sign
# 3. There are 3 words which are split up by the operator and the = sign
# 

# %%

# The puzzle has only one operator
def validate_operator(puzzle):
    pattern = r'^[^+\-*/]*[+\-*/][^+\-*/]*$'
    if re.match(pattern, puzzle):
        return True
    else:
        raise Exception("The cryptarithmetic puzzle is not in the correct form. Use one operator (+, -, *, /) to define your calculation.")

# the puzzle has an only one = sign
def validate_equal_sign(puzzle):
    if puzzle.count('=') == 1:
        return True
    else: 
        raise Exception('The cryptarithmetic puzzle is not in the correct form. Use one "=" sign.')
    
# The puzzle has 3 words which are split up by the operator and the = sign
def validate_3words(puzzle):
    pattern = r'^[a-zA-Z]+\s*[+\-*/]\s*[a-zA-Z]+\s*=\s*[a-zA-Z]+$'

    modified_string = re.sub(r'\s', '', puzzle)
    if re.match(pattern, modified_string) :
        return True
    else:
        raise Exception('The cryptarithmetic puzzle is not in the correct form. The correct form is: "ai + is = fun", you will need 3 words.')

# Execute all validation functions
def validate_puzzle(puzzle):
    validate_operator(puzzle)
    validate_equal_sign(puzzle)
    validate_3words(puzzle)


# %% [markdown]
# ### Getting the operator and the words
# The next step is to define a few things:
# 1. The operator ( +, -, *, / )
# 2. We need the 3 words, the first 2 words in the calculation and the result word.
# 

# %%
def find_operator(puzzle):
     if "+" in puzzle:
          operator = "+"
     elif "-" in puzzle:
          operator = "-"
     elif "*" in puzzle:
          operator = "*"
     else:
           operator = "/"
     return operator

# %% [markdown]
# For the words we slice the given puzzle. Because we defined the correct form of the puzzle as 'word1 + word2 = result', between the 2 first there is an operator and in between the 2 last words there is an equal sign. Because we know this, we can slice the puzzle by finding the operator and the equal sign. After slicing the puzzle we remove the spaces and we capitalize the letters.

# %%
def find_words(puzzle, operator):
    word_1 = puzzle[:puzzle.index(operator)].replace(" ","").upper()
    word_2 = puzzle[puzzle.index(operator)+1:puzzle.index("=")].replace(" ","").upper()
    word_result = puzzle[puzzle.index("=")+1:].replace(" ","").upper()
    return [word_1, word_2, word_result]


# %% [markdown]
# ### Unique letters and the possible numbers
# Next we want to create a tuple of all the unique letters. 

# %%
def find_letters(words):
    return tuple(set("".join(words)))

# %% [markdown]
# Also a dictionairy where each possible number is appointed to a letter. Of course the first letters of the words cannot have 0 as a value.

# %%
def possible_values(letters, words):
    domains = {}
    for letter in letters:
        if letter in [words[0][0], words[1][0], words[2][0]]:
            
            domains[letter] = list(range(1, 10))
        else:
            domains[letter] = list(range(0, 10))
    return domains


# %% [markdown]
# ### Constraints
# We need 2 constraints, one constraint to make sure that there are no duplicates. The other calculates the result of the operation and checks this with the given result. Because the constraints will need to be in a certain form, the program will have to calculate somethings that we have already calculated. 

# %%
# constraint 1
def constraint_unique(variables, values):
    return len(values) == len(set(values))

# helper function for constraint 2
def word_as_number(word, values, variables):
    number = ""
    for letter in word:
        number += str(values[variables.index(letter)])
    return int(number)

#constraint 2
def constraint_calculation(variables, values):
    operator = find_operator(puzzle)

    words = find_words(puzzle, operator)

    number_1 = word_as_number(words[0], values, variables)

    number_2 = word_as_number(words[1], values, variables)
    
    result = word_as_number(words[2], values, variables)

    if operator ==  "+":
        return (number_1 + number_2) == result
    elif operator == "-":
        return result == (number_1 - number_2) == result
    elif operator == "*":
        return (number_1 * number_2) == result
    else:
        return (number_1 / number_2) ==result

# %% [markdown]
# ## Output
# 
# I want the words and the numbers they represent in the output. So I create a function that gets me the numeric value of the words.
# 

# %%
def number_result(word : str,solutions : dict):
    number = ""
    for letter in word:
        number += str(solutions[letter])
    return int(number)

# %% [markdown]
# ### Solution
# All the previous functions will be used in the main fuction. This function will be used when puzzle has a value. This is important in streamlit to not get errors when loading the page

# %%
def main(puzzle):

    validate_puzzle(puzzle)

    operator = find_operator(puzzle)

    words = find_words(puzzle, operator)

    letters = find_letters(words)

    domains = possible_values(letters, words)
    
    constraints = [
        (letters, constraint_unique),
        (letters, constraint_calculation),
    ]
    problem = CspProblem(letters, domains, constraints)

    output = backtrack(problem)
    try:
        print(f"{words[0]} {operator} {words[1]} = {words[2]}\n"+ 
              f"{number_result(words[0], output)} {operator} {number_result(words[1], output)} = {number_result(words[2], output)}\n" + 
              "__________________________________________________________________\n")
        st.write(f"{words[0]} {operator} {words[1]} = {words[2]}")
        st.write(f"{number_result(words[0], output)} {operator} {number_result(words[1], output)} = {number_result(words[2], output)}")
    except:
        print("No solutions found\n"
              "__________________________________________________________________\n")
        st.write("No solutions found")



if puzzle:
    main(puzzle)


