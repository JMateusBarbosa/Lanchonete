
# 🍔 Sistema de Gerenciamento de Pedidos - Lanchonete

[🔗 Acesse a aplicação online aqui!](https://lanchonete-9i0z.onrender.com)

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11.1-blue" alt="Python Badge"/>
  <img src="https://img.shields.io/badge/Flask-3.0.3-orange" alt="Flask Badge"/>
  <img src="https://img.shields.io/badge/MySQL-8.0-blue" alt="MySQL Badge"/>
  <img src="https://img.shields.io/badge/Status-Finalizando-yellow" alt="Status Badge"/>
</p>

## 📑 Índice

- [Descrição do Projeto](#-descrição-do-projeto)
- [Status do Projeto](#-status-do-projeto)
- [Funcionalidades](#-funcionalidades)
- [Acesso ao Projeto](#-acesso-ao-projeto)
- [Configuração do Banco de Dados](#-configuração-do-banco-de-dados)
- [Tecnologias Utilizadas](#-tecnologias-utilizadas)
- [Pessoas Contribuidoras](#-pessoas-contribuidoras)
- [Licença](#-licença)

## 📖 Descrição do Projeto

Este é um sistema completo de gerenciamento de pedidos para lanchonetes, desenvolvido com o objetivo de otimizar o processo de anotar e acompanhamento de pedidos, além de fornecer relatórios detalhados de vendas. O sistema permite:

- Registro e visualização de pedidos.
- Acompanhamento do status dos pedidos em tempo real.
- Relatórios de vendas com filtros de data.
- Gestão do cardápio e feedback dos clientes.

## 🚧 Status do Projeto

🚀 **Finalizando:** O sistema está em fase de finalização, com suas funcionalidades parcialmente implementadas conforme os requisitos. Testes de desempenho e possíveis melhorias estão sendo feitos antes de lançar a verção final.

## 🛠️ Funcionalidades

- **Cadastro de Cardápio:** Permite adicionar, editar e excluir itens do cardápio.
- **Anotar Pedidos:** Registra os pedidos com informações da mesa ou cliente e calcula automaticamente o valor final.
- **Acompanhamento de Pedidos:** Exibe os pedidos em andamento, com a possibilidade de atualizar o status manualmente (Pendente, Concluído).
- **Relatório de Vendas:** Gera relatórios detalhados com base em um intervalo de datas, mostrando o total de vendas, total de pedidos, média por venda e produto mais vendido.
- **Feedback dos Clientes:** O usuário pode registrar notas e comentários de clientes ao finalizar o pedido.

## 🌐 Acesso ao Projeto

1. Clone o repositório:
   ```bash
   git clone https://github.com/JMateusBarbosa/Lanchonete.git
   ```
2. Acesse o diretório do projeto:
   ```bash
   cd sistema-lanchonete
   ```
3. Crie um ambiente virtual:
   ```bash
   python -m venv venv
   ```
4. Ative o ambiente virtual:
   - **Windows**:
     ```bash
     venv\Scripts\activate
     ```
   - **Linux/MacOS**:
     ```bash
     source venv/bin/activate
     ```
5. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
6. Configure o banco de dados conforme a seção [Configuração do Banco de Dados](#-configuração-do-banco-de-dados).   
7. Inicie o servidor localmente:
   ```bash
   python app.py
   ```
8. Acesse a aplicação em: `http://localhost:5000`.

## 🛠️ Configuração do Banco de Dados

Para configurar o banco de dados MySQL, execute os comandos SQL abaixo no MySQL Workbench ou em outra ferramenta de sua escolha:

```sql
CREATE TABLE itens_cardapio (
    id_item INT AUTO_INCREMENT PRIMARY KEY,
    nome_item VARCHAR(255) NOT NULL,
    descricao TEXT,
    preco DECIMAL(10, 2) NOT NULL,
    disponivel BOOLEAN NOT NULL DEFAULT TRUE,
    data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP,
    ultima_atualizacao DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE mesas (
    numero_mesa INT PRIMARY KEY,
    status_mesa VARCHAR(50) NOT NULL
);

CREATE TABLE pedidos (
    id_pedido INT AUTO_INCREMENT PRIMARY KEY,
    nome_cliente VARCHAR(255),
    numero_mesa INT,
    status ENUM('Pendente', 'Em Preparação', 'Concluído') NOT NULL DEFAULT 'Pendente',
    data_pedido DATETIME DEFAULT CURRENT_TIMESTAMP,
    total_pedido DECIMAL(10, 2),
    FOREIGN KEY (numero_mesa) REFERENCES mesas(numero_mesa)
);

CREATE TABLE itens_pedido (
    id_item_pedido INT AUTO_INCREMENT PRIMARY KEY,
    id_pedido INT,
    id_item INT,
    quantidade INT NOT NULL,
    preco_item DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (id_pedido) REFERENCES pedidos(id_pedido),
    FOREIGN KEY (id_item) REFERENCES itens_cardapio(id_item)
);

CREATE TABLE feedback (
    id_feedback INT AUTO_INCREMENT PRIMARY KEY,
    id_pedido INT,
    nota TEXT,
    FOREIGN KEY (id_pedido) REFERENCES pedidos(id_pedido)
);

CREATE USER 'lanchonete'@'localhost' IDENTIFIED BY '123456';
GRANT ALL PRIVILEGES ON lanchonete_db.* TO 'lanchonete'@'localhost';
FLUSH PRIVILEGES;

ALTER USER 'lanchonete'@'localhost' IDENTIFIED WITH mysql_native_password BY '123456';
FLUSH PRIVILEGES;
```


## 🛠️ Tecnologias Utilizadas

- **Python** - Linguagem principal para lógica de backend.
- **Flask** - Framework para desenvolvimento da API e lógica de servidor.
- **MySQL** - Banco de dados para armazenamento de pedidos, cardápio, e relatórios.
- **HTML5/CSS3** - Estruturação e estilização das páginas.
- **JavaScript** - Interatividade e manipulação do DOM para funcionalidades dinâmicas como acompanhamento de pedidos em tempo real (AJAX).
- **Bootstrap** - Framework para construção de layouts responsivos e adaptáveis.

## 🤝 Pessoas Contribuidoras

Este projeto foi desenvolvido individualmente até o momento, mas contribuições são bem-vindas!

## 📜 Licença

Este projeto está sob a licença [MIT](https://opensource.org/licenses/MIT).

---

<p align="center">Desenvolvido com 💻 e ☕ por João Mateus</p>
