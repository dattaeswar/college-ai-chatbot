const express = require("express");
const cors = require("cors");
const { GoogleGenerativeAI } = require("@google/generative-ai");

const app = express();
app.use(cors());
app.use(express.json());

// PUT YOUR GEMINI API KEY HERE
const genAI = new GoogleGenerativeAI("AIzaSyBcJL3ibc7FFWgKxWokDetJT62PtipRUFE");

// fast Gemini model
const model = genAI.getGenerativeModel({
  model: "gemini-2.0-flash"
});

// test route
app.get("/", (req, res) => {
  res.send("Gemini chatbot server running");
});

app.post("/chat", async (req, res) => {
  try {

    const userMessage = req.body.message;

    const prompt = `
You are an AI chatbot for GITAM University.

Rules:
- Only answer questions about GITAM University.
- If the question is unrelated say:
"I can only answer questions about GITAM University."
- Reply in maximum 3 bullet points.

User question: ${userMessage}
`;

    const result = await model.generateContent(prompt);

    const response = result.response;

    const reply = response.text();

    res.json({
      reply: reply
    });

  } catch (error) {

    console.log("===== GEMINI ERROR =====");
    console.log(error);

    res.json({
      reply: "Server error: " + error.message
    });

  }
});

app.listen(3000, () => {
  console.log("Server running on port 3000");
});