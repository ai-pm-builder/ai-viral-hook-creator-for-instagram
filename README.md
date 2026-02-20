# 🍔 Viral Hook Generator

A Streamlit web application that generates viral Instagram hooks for food content using Langflow AI integration. Simply describe your video idea, and the app will generate engaging hook recommendations to help your content go viral.

## ✨ Features

- **AI-Powered Hook Generation**: Uses Langflow API to generate creative and engaging hooks
- **Food Content Focus**: Specialized for Instagram food content creators
- **Beautiful UI**: Modern, responsive interface with gradient styling
- **Easy to Use**: Simple input form - just describe your video and get hooks
- **Copy Functionality**: One-click copy for each generated hook
- **Error Handling**: Graceful error messages and helpful troubleshooting tips

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Langflow API instance (local or remote)
- Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd "AI viral reel generator"
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   # Copy the example file
   cp .env.example .env
   
   # Edit .env file with your Langflow API details
   ```

5. **Update `.env` file**
   ```env
   LANGFLOW_API_URL=http://localhost:7860/api/v1/run
   LANGFLOW_API_KEY=your_langflow_api_key_here  # Optional
   GEMINI_API_KEY=your_gemini_api_key_here      # Required for Langflow workflow
   LANGFLOW_FLOW_ID=your_flow_id               # Optional
   ```
   
   **Note**: Get your Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)

6. **Run the application**
   ```bash
   streamlit run app.py
   ```

7. **Open your browser**
   - The app will automatically open at `http://localhost:8501`
   - If not, navigate to the URL shown in the terminal

## 📋 Usage

1. **Enter Video Description**: In the text area, describe the food video you want to create
   - Example: "A quick tutorial on making the perfect chocolate chip cookies with a secret ingredient that makes them extra chewy"

2. **Generate Hooks**: Click the "✨ Generate Hooks" button

3. **Review Results**: The app will display formatted hook recommendations

4. **Copy Hooks**: Click the "📋 Copy" button next to any hook you like

5. **Use in Your Content**: Paste the hooks into your Instagram posts or reels

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the project root with the following variables:

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `LANGFLOW_API_URL` | Langflow API endpoint URL | Yes | `http://localhost:7860/api/v1/run` |
| `LANGFLOW_API_KEY` | API key for authentication | No | (empty) |
| `GEMINI_API_KEY` | Gemini API key for Langflow workflow | Yes | (empty) |
| `LANGFLOW_FLOW_ID` | Specific flow ID to use | No | (empty) |
| `REQUEST_TIMEOUT` | Request timeout in seconds | No | `30` |

### Langflow Setup

1. **Local Langflow Instance**:
   - Install and run Langflow locally
   - Default API endpoint: `http://localhost:7860/api/v1/run`
   - Update `LANGFLOW_API_URL` in `.env` if using a different port

2. **Remote Langflow Instance**:
   - Use your deployed Langflow URL
   - Example: `https://your-langflow-instance.com/api/v1/run`
   - Update `LANGFLOW_API_URL` in `.env`

3. **Gemini API Key**:
   - Obtain your Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Add it to your `.env` file as `GEMINI_API_KEY`
   - This key is used within your Langflow workflow to power the AI hook generation

4. **Langflow Flow JSON**:
   - Place your Langflow flow JSON file in the project root as `langflow_flow.json`
   - The app will use this configuration when making API calls

## 📁 Project Structure

```
AI viral reel generator/
├── app.py                 # Main Streamlit application
├── langflow_client.py     # Langflow API integration module
├── config.py             # Configuration and environment variables
├── requirements.txt      # Python dependencies
├── README.md             # Project documentation
├── .env.example          # Example environment variables
├── .gitignore            # Git ignore rules
└── langflow_flow.json    # Langflow flow configuration (optional)
```

## 🛠️ Development

### Running in Development Mode

```bash
streamlit run app.py --server.port 8501
```

### Testing

1. Ensure Langflow API is running
2. Test with various video descriptions
3. Check error handling with invalid API URLs
4. Verify hook parsing with different response formats

## 🐛 Troubleshooting

### Common Issues

**Issue**: "Could not connect to Langflow API"
- **Solution**: Check if Langflow is running and verify the `LANGFLOW_API_URL` in `.env`

**Issue**: "Request timed out"
- **Solution**: Increase `REQUEST_TIMEOUT` in `.env` or check your network connection

**Issue**: "Invalid JSON response"
- **Solution**: Verify your Langflow flow is returning valid JSON responses

**Issue**: No hooks displayed
- **Solution**: Check the Langflow response format. The app tries multiple parsing strategies, but you may need to adjust `parse_hooks_response()` in `langflow_client.py`

### Getting Help

1. Check the Langflow API documentation
2. Verify your `.env` configuration
3. Check the Streamlit terminal for detailed error messages
4. Review the Langflow flow JSON structure

## 📝 License

This project is open source and available for anyone to use and modify.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Support

For issues or questions, please open an issue on the GitHub repository.

---

**Made with ❤️ for food content creators**
