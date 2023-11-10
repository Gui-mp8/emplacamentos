# Emplacamentos Analysis

This project has the goal to integrate car data, that comes from 3 diferent sources, that we can make an analyse from it.

## Tecnologies
<table>
    <tr>
        <td>Linux</td>
        <td>Code</td>
        <td>Container</td>
        <td>DataBase</td>
        <td>Visualization</td>
    </tr>
    <tr>
        <td>Ubuntu</td>
        <td>Python</td>
        <td>Docker</td>
        <td>BigQuery</td>
        <td>Google Looker Studio</td>
    </tr>
</table>

## Prerequisite

Before running the project, make sure you have the following tools installed:

- [Python](https://www.python.org/downloads/)

- [Docker](https://docs.docker.com/engine/install/ubuntu/)

- [docker compose plugin](https://docs.docker.com/compose/install/linux/#install-using-the-repository) atualizado

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
3. Running the tests

    ```
    $ pytest tests/
    ```
4. Run the following command to execute the code

    ```
    $ make run
    ```

**OBS:** If you want to delete the directories created, you can use teh comand
```
$ cd data && sudo rm -rf {directory} && cd ..
```