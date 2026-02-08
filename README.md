# 🚀 InterviewGenie: AI-Driven Recruitment Ecosystem

**InterviewGenie** is a next-generation career tool that bridges the gap between candidates and recruiters. Powered by **Gemini 3 Flash**, it provides real-time interview coaching and high-speed resume ranking using vector search.

---

## ✨ Key Features

### 👤 For Candidates (Candidate Portal)
- **AI Resume Analysis:** Deep-scan resumes for ATS compatibility, keywords, and formatting.
- **Skill Radar Mapping:** Visual representation of technical and soft skills using Chart.js.
- **AI Interview Room:** Practice interviews with a real-time AI coach that gives instant feedback.

### 🏢 For Recruiters (Recruiter Mode)
- **Bulk Resume Ranking:** Upload hundreds of CVs and rank them against a job description in seconds.
- **FAISS Vector Search:** Uses Facebook AI Similarity Search (FAISS) to find the best semantic match, not just keyword matching.
- **High-Speed Embeddings:** Leverages `sentence-transformers` for deep document understanding.

---

## 🛠 Tech Stack

- **Backend:** Python (Flask)
- **AI Engine:** Google Gemini 3 Flash API
- **Vector Database:** FAISS (Facebook AI Similarity Search)
- **Embeddings:** Sentence-Transformers (`all-MiniLM-L6-v2`)
- **Frontend:** Tailwind CSS, JavaScript (ES6+), Chart.js
- **Processing:** PyPDF2, Docx2txt

---

## How it Works (Logic Flow)

- Text Extraction: Resumes are parsed and cleaned from PDF/DOCX formats.
- Vectorization: Text is converted into numerical embeddings (vectors).
- Similarity Search: When a recruiter enters a Job Description, FAISS calculates the "Cosine Similarity" between the JD and all uploaded resumes.
- Ranking: Candidates are ranked based on their semantic score, ensuring the most relevant talent is always at the top.




 
