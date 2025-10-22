# Flowise Prompt Template: Vacancy Analysis and Solution Proposal

This document outlines the expected input format for a Flowise chatflow designed to analyze job vacancies and generate a tailored solution proposal. It also describes the desired output format.

## 1. Input Structure for Flowise Chatflow

The Flowise chatflow will receive a JSON object containing the parsed vacancy data and initial analysis from the Python agent. The `question` field in the Flowise API request will contain a stringified version of this JSON.

**Example Input JSON:**

```json
{
  "vacancy_title": "Senior Python Developer",
  "company": "ExampleTech Solutions",
  "description": "We are seeking a highly skilled Senior Python Developer to lead our backend development efforts. The ideal candidate will be responsible for designing, developing, and maintaining scalable web applications, optimizing database performance, and mentoring junior developers. Experience with cloud platforms (AWS, GCP) and CI/CD pipelines is essential. KPI: Reduce system latency by 20% within 6 months.",
  "requirements": "5+ years of Python development experience, strong knowledge of Django/FastAPI, PostgreSQL, Docker, AWS/GCP, Git. Excellent problem-solving skills and ability to work in an Agile environment.",
  "parsed_data": {
    "key_responsibilities": [
      "designing, developing, and maintaining scalable web applications",
      "optimizing database performance",
      "mentoring junior developers"
    ],
    "technical_requirements": [
      "Python", "Django", "FastAPI", "PostgreSQL", "Docker", "AWS", "GCP", "Git"
    ],
    "kpis": [
      "Reduce system latency by 20% within 6 months"
    ],
    "seniority_level": "senior"
  }
}
```

## 2. Expected Output Structure from Flowise Chatflow

The Flowise chatflow is expected to return a JSON object (or a plain text response that can be parsed) containing the generated solution proposal and potentially other structured insights.

**Example Output (JSON format preferred):**

```json
{
  "proposal_text": "Dear Hiring Manager,\n\nThank you for sharing the exciting opportunity for a Senior Python Developer at ExampleTech Solutions.\n\nBased on our analysis, we understand that you are looking for a specialist to lead backend development, focusing on scalable web applications, database optimization, and team mentorship. Your key technical requirements include Python, Django/FastAPI, PostgreSQL, Docker, and cloud platforms like AWS/GCP, with a critical KPI to reduce system latency by 20% within six months.\n\nOur team of full-stack experts possesses deep experience in these areas. We propose a solution focused on:\n1.  **Strategic Architecture Review**: Assessing current systems to identify bottlenecks and design highly performant, scalable solutions.\n2.  **Performance Optimization**: Implementing advanced database tuning, efficient caching strategies, and optimizing code paths to directly address the latency reduction KPI.\n3.  **Mentorship & Best Practices**: Providing senior-level guidance and implementing robust CI/CD practices to elevate team capabilities and ensure long-term maintainability.\n\nWe are confident in our ability to not only meet but exceed your performance objectives. We would be delighted to schedule a technical deep-dive with our lead architect to discuss a tailored implementation plan and demonstrate how we can help achieve your goals.\n\nPlease let us know your availability for a brief call.\n\nBest regards,\n[Your Company/Agent Name]",
  "extracted_keywords": ["Python", "Django", "FastAPI", "AWS", "GCP", "latency reduction", "scalable web applications"],
  "sentiment": "positive"
}
```

**Alternatively, a plain text output is also acceptable if structured parsing is handled by the Python agent:**

```
Dear Hiring Manager,

Thank you for sharing the exciting opportunity for a Senior Python Developer at ExampleTech Solutions.

Based on our analysis, we understand that you are looking for a specialist to lead backend development, focusing on scalable web applications, database optimization, and team mentorship. Your key technical requirements include Python, Django/FastAPI, PostgreSQL, Docker, and cloud platforms like AWS/GCP, with a critical KPI to reduce system latency by 20% within six months.

Our team of full-stack experts possesses deep experience in these areas. We propose a solution focused on:
1.  **Strategic Architecture Review**: Assessing current systems to identify bottlenecks and design highly performant, scalable solutions.
2.  **Performance Optimization**: Implementing advanced database tuning, efficient caching strategies, and optimizing code paths to directly address the latency reduction KPI.
3.  **Mentorship & Best Practices**: Providing senior-level guidance and implementing robust CI/CD practices to elevate team capabilities and ensure long-term maintainability.

We are confident in our ability to not only meet but exceed your performance objectives. We would be delighted to schedule a technical deep-dive with our lead architect to discuss a tailored implementation plan and demonstrate how we can help achieve your goals.

Please let us know your availability for a brief call.

Best regards,
[Your Company/Agent Name]
```

## 3. Flowise Chatflow Design Considerations

When designing the chatflow in Flowise, consider the following:

*   **LLM Selection**: Choose an appropriate LLM (e.g., GPT-4.1-mini, gemini-2.5-flash) for text generation and summarization.
*   **Prompt Engineering**: Craft effective prompts to guide the LLM in generating relevant and persuasive proposals.
*   **Chain Structure**: Use chains to perform sequential tasks:
    1.  Receive raw vacancy data.
    2.  Extract key information (if not fully done by Python agent).
    3.  Generate a tailored solution proposal.
    4.  (Optional) Extract keywords or sentiment for further analysis.
*   **Tools**: Consider integrating tools within Flowise for:
    *   **Vector Database Lookup**: To retrieve relevant case studies or project examples based on vacancy requirements.
    *   **Knowledge Base**: To provide context on your team's capabilities and offerings.
*   **Output Formatting**: Ensure the output is consistently formatted for easy consumption by the Python agent.
