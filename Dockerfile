# Use uma imagem oficial do Python como imagem base.
# Usar a versão 'slim' ajuda a manter o tamanho da imagem final menor.
FROM python:3.9-slim

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia o arquivo de dependências para o diretório de trabalho.
# Fazemos isso primeiro para aproveitar o cache de camadas do Docker.
# A camada de instalação de dependências só será reconstruída se o requirements.txt mudar.
COPY requirements.txt .

# Instala as dependências definidas no requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código da aplicação para o diretório de trabalho
COPY . .

# Expõe a porta 8000 para que o Gunicorn possa ser acessado de fora do contêiner
EXPOSE 8000

# Comando para executar a aplicação usando o servidor Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]