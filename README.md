# AntiScamBot

Este é um bot do Discord desenvolvido para detectar e remover links suspeitos de mensagens enviadas em servidores do Discord. Ele utiliza uma lista de links bloqueados que é carregada de um repositório GitHub.

## Funcionalidades

- Detecta e remove mensagens contendo links suspeitos.
- Notifica um canal específico sobre a remoção de mensagens suspeitas.
- Permite que administradores definam o canal de notificação.

## Como usar

### Pré-requisitos

- Python 3.8 ou superior
- Biblioteca `discord.py`
- Biblioteca `requests`

### Instalação

1. Clone este repositório:
   ```bash
   git clone https://github.com/pglesv/AntiScamBot.git
   ```
2. Navegue até o diretório do projeto:
   ```bash
   cd AntiScamBot
   ```
3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

### Configuração

1. Substitua `'YOUR_TOKEN_HERE'` pelo token do seu bot no arquivo `bot.py`.
⚠️ Altere e use .env caso esteja usando em algum lugar publico.

### Executando o Bot

1. Execute o bot:
   ```bash
   python bot.py
   ```

## Comandos

- `!definir_canal_notificar <canal>`: Define o canal onde as notificações de links suspeitos serão enviadas. Este comando só pode ser usado por administradores.

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e enviar pull requests.

## Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
