# 🍔 Viral Hook Generator

A professional-grade Streamlit web application that generates viral Instagram hooks for food content using a specialized **4-Prompt LangChain Workflow**. Simply describe your recipe or video idea, and the system will generate, test, rank, and finalize the most high-performance hook for your audience.

## ✨ Features

- **Strategic LangChain Workflow**: Moves beyond simple generation to include persona testing and scoring.
- **Advanced Persona Simulation**: Tests hooks against a "Priya" persona—a 28-year-old Indian woman mid-scroll.
- **Evidence-Based Ranking**: Uses content strategist logic to score hooks on Hold Rate, Watch Time, and Shareability.
- **Production-Ready Output**: Generates a "Production Card" with exact spoken VO, text overlays, and visual setup.
- **Beautiful UI**: Premium gradient-styled Streamlit interface for a professional experience.

## 🧠 Workflow & Logic

The system operates using a **Sequential LangChain Chain** that simulates a full creative agency process:

1.  **Viral Hook Generation**: Brainstorms 5 unique hooks using 6 proven psychological patterns (Neurological Pattern Interrupt, Loss Aversion, Curiosity Gap, Time-Collapse, Identity-Targeted, and Social Proof).
2.  **Priya Persona Simulation**: The AI inhabits the life of a specific audience member ("Priya") to provide an "unfiltered" reaction to each hook, including internal monologues and scroll/watch decisions.
3.  **Evidence-Based Scoring**: A Senior Content Strategist agent analyzes the simulation data to score each hook out of 37 points, focusing on 3-second hold rate, watch time potential, and share probability.
4.  **Production Card Finalization**: The winning hook is "surgically" improved and converted into a ready-to-shoot production brief with text overlay guides, spoken scripts, and visual frame descriptions.

## 🛠️ Tools Used

- **LangChain**: The core framework used to architect the sequential chain and manage prompt inputs/outputs.
- **Google Gemini 2.5 Flash**: The generative engine powering all 4 stages of the workflow with high-speed reasoning.
- **Streamlit**: Used to build the modern, interactive frontend.
- **Python Dotenv**: Manages sensitive API keys and configuration.

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd "AI viral reel generator"
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   Create a `.env` file in the root directory:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   REQUEST_TIMEOUT=60
   ```

4. **Run the application**
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


**Issue**: "Request timed out"
- **Solution**: Increase `REQUEST_TIMEOUT` in `.env` or check your network connection

**Issue**: "Invalid JSON response"
- **Solution**: Verify your Langchain flow is returning valid JSON responses

**Issue**: No hooks displayed
- **Solution**: Check the Langchain response format. The app tries multiple parsing strategies, but you may need to adjust `parse_hooks_response()` in `langchain_client.py`

### Getting Help

1. Check the Langchain API documentation
2. Verify your `.env` configuration
3. Check the Streamlit terminal for detailed error messages
4. Review the Langchain flow JSON structure

## 📝 License

This project is open source and available for anyone to use and modify.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Support

For issues or questions, please open an issue on the GitHub repository.

---

**Made with ❤️ for food content creators**
