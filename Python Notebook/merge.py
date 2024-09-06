import nbformat

# Lista de arquivos .ipynb para mesclar
notebooks = ["module_01.ipynb", "module_02.ipynb", "module_03.ipynb", "module_04.ipynb", "module_05.ipynb",
             "module_06.ipynb", "module_07.ipynb", "module_08.ipynb", "module_09.ipynb", "module_10.ipynb"]

# Cria um novo notebook vazio
merged_notebook = nbformat.v4.new_notebook()

# Itera sobre cada notebook na lista
for notebook_filename in notebooks:
    with open(notebook_filename, 'r', encoding='utf-8') as file:
        # Lê o notebook
        notebook = nbformat.read(file, as_version=4)
        
        # Adiciona todas as células do notebook lido ao novo notebook
        merged_notebook.cells.extend(notebook.cells)

# Salva o notebook mesclado em um novo arquivo
with open("Python.ipynb", 'w', encoding='utf-8') as file:
    nbformat.write(merged_notebook, file)

print("Notebooks unidos com sucesso!")