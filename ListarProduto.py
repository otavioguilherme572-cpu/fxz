ARQUIVO = "produtos.txt"

# Solicita os dados de um novo produto e salva o cadastro no arquivo.
def cadastrar_produto():
    nome = input("Digite o nome do produto: ").strip()
    codigo_barras = input("Digite o código de barras: ").strip()
    preco = input("Digite o preço (ex: 49.90): ").strip()
    descricao = input("Digite a descrição do produto: ").strip()

    # Validação básica: nome e código de barras não podem ficar vazios.
    if not nome or not codigo_barras:
        print("Erro: Nome do produto e Código de barras são obrigatórios.")
        return

    # Salva os dados separados por ponto e vírgula no arquivo.
    with open(ARQUIVO, "a", encoding="utf-8") as f:
        f.write(f"{nome};{codigo_barras};{preco};{descricao}\n")
    print(f"Produto '{nome}' cadastrado com sucesso!")

# Lê e exibe todos os produtos armazenados no arquivo.
def listar_produtos():
    try:
        with open(ARQUIVO, "r", encoding="utf-8") as f:
            linhas = f.readlines()
            if not linhas:
                print("Nenhum produto cadastrado.")
                return

            print("\n--- Produtos Cadastrados ---")
            for i, linha in enumerate(linhas, 1):
                dados = linha.strip().split(";")
                if len(dados) == 4:
                    nome, codigo_barras, preco, descricao = dados
                    print(f"{i}. Produto: {nome} | Cód. Barras: {codigo_barras} | Preço: R$ {preco}")
                    print(f"   Descrição: {descricao}")
                    print("-" * 40)
    except FileNotFoundError:
        print("Arquivo de registros ainda não existe. Faça um cadastro primeiro.")

# Exibe as opções do sistema e direciona cada escolha para a função correspondente.
def menu():
    while True:
        print("\n=== SISTEMA DE CADASTRO DE PRODUTOS ===")
        print("1. Cadastrar produto")
        print("2. Listar produtos")
        print("3. Sair")
        
        opcao = input("Escolha uma opção: ").strip()
        
        if opcao == "1":
            cadastrar_produto()
        elif opcao == "2":
            listar_produtos()
        elif opcao == "3":
            print("Encerrando o programa.")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    menu()