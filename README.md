# Emplacamentos Analysis

This project has the goal to integrate car data, that comes from 3 diferent sources, that we can make an analyse from it.

## Tecnologies
<table>
    <tr>
        <td>Linux</td>
        <td>Code</td>
        <td>DataBase</td>
        <td>Visualization</td>
    </tr>
    <tr>
        <td>Ubuntu</td>
        <td>Python</td>
        <td>BigQuery</td>
        <td>Google Looker Studio</td>
    </tr>
</table>

## Prerequisite

Before running the project, make sure you have the following tools installed:

- [Python](https://www.python.org/downloads/)

## Execution

Follow the steps below to run the project:

1. Clone the repository:

    ```
    $ git clone git@github.com:Gui-mp8/emplacamentos.git
    ```

2. Access the project directory:

    ```
    $ cd emplacamentos
    ```
3. Create the python environment

    ```
    $ python3 -m venv venv
    $ source venv/bin/activate
    $ pip install -r requiriments.txt
    ```

4. Running the tests

    ```
    $ pytest tests/
    ```
5. Run the following command to execute the code

    ```
    $ python3 src/main.py
    ```