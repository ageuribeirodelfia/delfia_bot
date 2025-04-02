# Usa a imagem oficial do Python como base
FROM python:3.13.1

# Define o diretório de trabalho no contêiner
WORKDIR /app

# Copia apenas o requirements.txt inicialmente (para otimizar cache)
COPY requirements.txt ./

# Remove a biblioteca específica antes da instalação
RUN grep -v "pywin32" requirements.txt > requirements-filtered.txt

# Instala as dependências do Python
RUN pip install --no-cache-dir -r requirements-filtered.txt

# Copia o restante do código para o contêiner
COPY . .

# Expõe a porta onde a aplicação vai rodar
EXPOSE 5000

# Define o comando padrão para iniciar a aplicação
CMD ["python", "main.py"]
