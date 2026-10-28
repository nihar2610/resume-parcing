
import { useState } from "react";
import "./App.css";

const API_URL = "http://127.0.0.1:8000/api/team/v1/resumes/extract";

function App() {
  const [file, setFile] = useState(null);
  const [hostedConsent, setHostedConsent] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(event) {
    event.preventDefault();

    if (!file) {
      setError("Please select a PDF or DOCX resume.");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    const formData = new FormData();
    formData.append("file", file);
    formData.append("hosted_consent", String(hostedConsent));

    try {
      const response = await fetch(API_URL, {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Resume extraction failed. Please try again."
        );
      }

      setResult(data);
    } catch (err) {
      setError(
        err.message.includes("Failed to fetch")
          ? "Cannot connect to the backend. Make sure your FastAPI server is running."
          : err.message
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="app">
      <header className="header">
        <div className="brand">RADIX</div>
        <span className="header-label">RESUME INTELLIGENCE</span>
      </header>

      <section className="hero">
        <p className="eyebrow">SMART RESUME ANALYSIS</p>
        <h1>Turn resumes into structured data.</h1>
        <p className="subtitle">
          Upload a resume to extract candidate details, skills,
          education, projects and experience.
        </p>
      </section>

      <section className="panel">
        <h2>Upload resume</h2>
        <p className="muted">Supported formats: PDF and DOCX · Maximum 5 MB</p>

        <form onSubmit={handleSubmit}>
          <label className="upload-box">
            <span className="upload-icon">↑</span>
            <strong>{file ? file.name : "Choose a resume file"}</strong>
            <span className="muted">Click here to browse your files</span>
            <input
              type="file"
              accept=".pdf,.docx,application/pdf,application/vnd.openxmlformats-officedocument.wordprocessingml.document"
              onChange={(event) => {
                setFile(event.target.files?.[0] || null);
                setResult(null);
                setError("");
              }}
            />
          </label>

          <label className="consent">
            <input
              type="checkbox"
              checked={hostedConsent}
              onChange={(event) => setHostedConsent(event.target.checked)}
            />
            <span>
              <strong>Use AI-powered extraction</strong>
              <small>
                I consent to sending the resume text to the hosted AI service
                (Groq) for extraction. Leave unchecked for manual extraction.
              </small>
            </span>
          </label>

          <button type="submit" disabled={loading}>
            {loading ? "Extracting resume..." : "Extract resume details"}
          </button>
        </form>

        {error && <div className="error">{error}</div>}
      </section>

      {result && (
        <section className="results">
          <div className="results-heading">
            <div>
              <p className="eyebrow">EXTRACTION COMPLETE</p>
              <h2>Candidate overview</h2>
            </div>
            <span className="status">{result.review_status || "processed"}</span>
          </div>

          <div className="details-grid">
            <Detail label="Candidate name" value={result.name} />
            <Detail label="Email" value={result.email} />
            <Detail label="Company" value={result.company} />
            <Detail label="Role" value={result.role} />
            <Detail label="Extraction method" value={result.extraction_method} />
            <Detail label="Schema version" value={result.schema_version} />
          </div>

          <ResultList title="Skills" items={result.skills} />
          <ResultList title="Education" items={result.education} />
          <ResultList title="Projects" items={result.projects} />
          <ResultList title="Experience" items={result.experience} />
          <ResultList title="Internships" items={result.internships} />
          <ResultList title="Certifications" items={result.certifications} />
          <ResultList title="Achievements" items={result.achievements} />
          <ResultList title="Warnings" items={result.warnings} />
        </section>
      )}

      <footer>RADIX · Resume Parsing Module · TEAM-V1</footer>
    </main>
  );
}

function Detail({ label, value }) {
  return (
    <div className="detail">
      <span>{label}</span>
      <strong>{value || "Not found"}</strong>
    </div>
  );
}

function ResultList({ title, items }) {
  if (!items || items.length === 0) return null;

  return (
    <section className="result-list">
      <h3>{title}</h3>
      {items.map((item, index) => (
        <div className="result-item" key={`${title}-${index}`}>
          {typeof item === "string" ? (
            item
          ) : (
            <div>
              <strong>{item.skill_name || item.title || "Item"}</strong>
              {item.category_code && (
                <span className="tag">{item.category_code}</span>
              )}
              {item.evidence && <p>{item.evidence}</p>}
              {item.confidence && (
                <small>Confidence: {item.confidence}</small>
              )}
              {item.claim_status && (
                <small> · Status: {item.claim_status}</small>
              )}
            </div>
          )}
        </div>
      ))}
    </section>
  );
}

export default App;
