# Interpreter-based KPI Evaluation

A Django-based application for managing and evaluating Key Performance Indicators (KPIs) linked to assets. The app allows creation, linkage, and evaluation of KPIs based on custom expressions and supports a simple interpreter for expression evaluation.

## Python Version 
- 3.10.0

## Modules

- `/kpi_app`: Main Django app handling KPI and asset management, expression parsing, and evaluation logic.
  - `/interpreter`: Contains modules for parsing and interpreting KPI expressions.
    - `lexer.py`: Tokenizes expressions for parsing.
    - `parser.py`: Parses tokens into an Abstract Syntax Tree (AST) for evaluation.
    - `interpreter.py`: Evaluates parsed expressions using visitor patterns.
  - `/migrations`: Contains migration files for database schema changes.
  - `models.py`: Defines models for KPI, KPIAssetLink, and EvaluationResult to store KPI data, linked assets, and evaluation results.
  - `serializers.py`: Serializes models for API responses.
  - `urls.py`: Defines URL routes for the API endpoints.
  - `views.py`: Implements API views for KPI creation, listing, asset linkage, and evaluation.
  - `admin.py`: Registers models to the Django admin interface for easy management.
  - `tests.py`: Contains test cases for KPI creation, linkage, and evaluation functionalities.
  - `utils.py`: Utility functions for processing and evaluating KPI expressions.

- `settings.py`: Configuration for the Django project, including installed apps, middleware, and database settings.
- `urls.py`: Defines project-level URL routes.

## Setup

### Install required dependencies

```
pip install -r requirements.txt
```

### Apply database migrations

```
python manage.py migrate
```

### Run the Django development server

```
python manage.py runserver
```

# Interpreter refactoring details

## Tokenization Process

#### Original Issue
The tokenization process was limited in flexibility. Each token type was hardcoded into the Lexer class, making it difficult to extend or add new token types.

#### Solution 
The refactored code introduces the Chain of Responsibility pattern. Each handler is responsible for identifying a specific type of token, and they are linked in a chain. 

#### Benefits
`Single Responsibility Principle:` Each handler is responsible for one type of token, reducing the complexity of the Lexer.
`Open-Closed Principle:` The chain can be extended to handle new token types without modifying existing handlers, making it open for extension but closed for modification.


## Creating operations

#### Original Issue
The original interpreter class directly handled arithmetic operations, but if new operations (like modulus) needed to be added, the interpreter class would require modification.

#### Solution in Refactored Code
The OperatorFactory class is introduced to handle the creation of binary operations, allowing for the addition of new operations without modifying the core interpreter code.

#### Benefits
`Open-Closed Principle:` New operations can be added by extending the OperatorFactory without modifying the core Interpreter class.

## Abstract Syntax Tree (AST) and Intepreter

#### Original Issue
In the original code, the AST node classes were defined but lacked a clear separation of visitor logic. 

#### Solution in Refactored Code
Each node type is defined as a subclass of ASTNode, and and the interpretation is handled through a Visitor Pattern

#### Benefits
`Maintainability:` Each operation on nodes is encapsulated in the visitor, making the code easier to understand and maintain.

## Parsing 

#### Original Issue
Parsing was relatively simple and handled basic precedence but lacked flexibility. Expanding it for more complex precedence rules would be challenging.

#### Solution in Refactored Code
The refactored parser introduces a PRECEDENCE dictionary and methods to parse expressions based on precedence levels.

#### Benefits
`Extensibility:` Precedence levels make it easier to add new operators with different levels of precedence.
`Readability:` The precedence-based parsing logic is easier to understand and maintain.


## UML Digarams
### Lexer
![dLB1IiGm4BtFL-HOaVv0yR171K5HxsLCXswnJfR9x1BG_NURJIn6SjdsKf9vRsRUozjvHT7ZvmpuxbNGgh4pUc_Ut0VnFV8mavWlCCjtQvY2zljqsHMG34YrPgOG0O_nTzEPavi6E0EapW-iD9AKlUlKF0FEcVgo4CCMujE11DLj6lgCgYIyXVggCl5u7HEWiFxkkst_MLO1hCR](https://github.com/user-attachments/assets/8b3259cb-814d-4a9a-aa9f-1ffd4d6aa488)

### Interpreter
![pLF1JeGm4BttA-OcneGFQ8nPlNbP4qMlcmgpIoEqJJjTbwZ_hYrB0UMWU_84y_fuCszUMJaIbdpRCAa8xLQK26jTuPDqahI5DmO0S07xK6-UfTfeawal0eSRgUxCEGUXkXb9-VR8MFjsuTmhORjHvZ6KYq8MTtWOYVUXJCGFnif6E0UtOMvZaV2_Jfk8SXWr8ul8uVgX2BiU7Pq](https://github.com/user-attachments/assets/4bf30e51-3ed9-4182-9543-1fb094f171ed)




