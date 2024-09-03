### Chat with SQL
A Streamlit-based application that allows users to interact with a MySQL database through natural language queries with the help of Mistral AI and Google Palm

## Prototype 
https://github.com/user-attachments/assets/c7390fd1-85ef-42bf-ad29-33dec41c4d57

### Description
- **Overview**: This application enables users to chat with a SQL assistant that interprets natural language questions and generates SQL queries to fetch data from a MySQL database. It then provides natural language responses based on the SQL query results.

### Features
- **Interactive Chat Interface**: Users can input questions in natural language, and the app generates corresponding SQL queries.
- **Streamlit Sidebar**: The sidebar allows users to configure database connection settings (host, port, username, password, and database name).
- **Real-time Database Interaction**: Once connected, users can query the database and get instant results displayed in a chat format.
- **Powered by LangChain and GooglePalm**: The app uses LangChain for prompt templates and GooglePalm for generating SQL queries from natural language inputs.

### Installation
1. **Clone the Repository**: 
   ```bash
   git clone <repository-url>
   ```
2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Set Up Environment Variables**:
   - Create a `.env` file and add your Google API key:
     ```plaintext
     GOOGLE_API_KEY=your_google_api_key
     ```

### Usage
1. **Run the Application**:
   ```bash
   streamlit run app.py
   ```
2. **Configure Database**: Use the sidebar to input your database credentials and connect.
3. **Start Chatting**: Type your query in the chat input, and the AI assistant will respond with the SQL query and the corresponding results.

### Dependencies
- **Python Packages**: 
  - Streamlit
  - MySQL Connector
  - LangChain
  - dotenv

### Contributing
- Contributions are welcome! Please submit a pull request or open an issue for suggestions and bug reports.

### License
- Provide the license under which your project is distributed (e.g., MIT License).

This outline provides a comprehensive overview of your project and guides users through setup and usage.
