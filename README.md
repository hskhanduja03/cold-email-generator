# 📧 Cold Mail Generator

Cold email generator for service-based companies using **Groq**, **LangChain**, and **Streamlit**. This tool allows users to input the URL of a company's careers page, extract job listings, and generate **personalized cold emails**. These emails also include relevant **portfolio links** pulled from a **vector database**, based on the specific job description.

---

## 🔍 Imagine This

- A company needs a Principal Software Engineer and is investing time and money in hiring, onboarding, and training.
- Instead of waiting, you (as a service provider) can offer a dedicated engineer directly to them.
- This tool helps generate a personalized cold email — backed by intelligent context from their job listings and your relevant work.

---

## 🏗️ Architecture Diagram

![Architecture](imgs/architecture.png)

---

## ⚙️ Setup Instructions

1. **Get an API Key**  
   Visit [https://console.groq.com/keys](https://console.groq.com/keys) and generate your Groq API key.

   Create a `.env` file inside the `app/` directory and add:
