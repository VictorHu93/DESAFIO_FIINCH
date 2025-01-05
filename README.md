# Desafio Jurídico com Django e RabbitMQ

Este projeto foi desenvolvido como parte de um desafio técnico, integrando Django, RabbitMQ, PostgreSQL e ferramentas de extração de dados de PDFs. O objetivo é criar um sistema que permita o upload de PDFs, a extração de informações estruturadas e o processamento assíncrono das informações através de mensageria.

---

## **Funcionalidades**

- **Upload de PDFs**: Interface para envio de PDFs para processamento.
- **Extração de Dados**: Extração de informações como número do processo, status, autor, e réus a partir de arquivos PDF.
- **Mensageria Assíncrona**: Integração com RabbitMQ para processamento de mensagens de forma assíncrona.
- **Geração de Planilhas**: Criação automática de planilhas diárias com os dados extraídos dos processos.
- **API REST**: Endpoints para listar dados extraídos e verificar a fila do RabbitMQ.

---

## **Tecnologias Utilizadas**

### **Backend**
- Django 5.1
- Django REST Framework
- PyPDF2 (Extração de dados de PDFs)

### **Mensageria**
- RabbitMQ 3 (com Management Plugin)

### **Banco de Dados**
- PostgreSQL 15

### **Frontend**
- Bootstrap 5
- JQuery

### **Outras Ferramentas**
- Docker e Docker Compose
- Testes automatizados com Django TestCase

---

## **Configuração Inicial**

### **1. Clonar o Repositório**
```bash
git clone https://github.com/VictorHu93/DESAFIO_FIINCH.git
cd seu-repositorio
```

### **2. Configurar Variáveis de Ambiente**
Crie um arquivo `.env` na raiz do projeto com o seguinte conteúdo:
```env
DATABASE_NAME=juridicos_db
DATABASE_USER=postgres
DATABASE_PASSWORD=postgres
RABBITMQ_USER=guest
RABBITMQ_PASSWORD=guest
RABBITMQ_HOST=rabbitmq
QUEUE_NAME=pdf_queue
```

### **3. Construir e Iniciar os Containers**
Certifique-se de que o Docker e o Docker Compose estão instalados e execute:
```bash
docker-compose up --build
```
Isso iniciará os serviços:
- **PostgreSQL** na porta `5432`
- **RabbitMQ** nas portas `5672` (mensageria) e `15672` (interface de gerenciamento)
- **Django App** na porta `8000`

### **4. Aplicar Migrações**
Dentro do container do app, execute:
```bash
docker-compose run app python manage.py migrate
```

### **5. Acessar a Interface**
- Interface de Upload: [http://localhost:8000/uploads/]
- Interface do RabbitMQ: [http://localhost:15672/]

---

## **Como Usar**

### **Upload de PDFs**
1. Acesse a página de upload: [http://localhost:8000/uploads/]
2. Selecione de 1 a 5 arquivos PDF.
3. Clique em "Enviar".

Os arquivos serão processados e enviados para a fila RabbitMQ. Os dados extraídos serão salvos no banco de dados.

### **Geração de Planilhas**
Após o upload dos PDFs, uma planilha será gerada automaticamente no diretório `data/`, com os dados extraídos dos processos enviados no dia.

### **API REST**
- **Listar Dados Extraídos**: [http://localhost:8000/uploads/api/data/]
- **Contagem de Mensagens na Fila**: Incluído na resposta do endpoint acima.

---

## **Testes Automatizados**

### **Executar Testes**
Dentro do container do app, execute:
```bash
docker-compose run app python manage.py test
```

### **Cobertura de Testes**
Os testes abrangem:
- **Models**: Testes para `ProcessosPDF` e `ProcessInfo`.
- **Views**: Testes para upload de PDFs e listagem de dados.
- **Consumer**: Testes para processamento de mensagens do RabbitMQ.

## **Conclusão**
Este projeto demonstra uma integração eficiente entre Django, RabbitMQ e PostgreSQL, criando um sistema robusto para processamento de dados jurídicos. Além de ser funcional, o projeto segue boas práticas de desenvolvimento, como separação de responsabilidades e uso de mensageria assíncrona.