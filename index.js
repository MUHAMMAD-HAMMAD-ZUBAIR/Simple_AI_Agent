#!/usr/bin/env node

const { execSync } = require("child_process");
const fs = require("fs");
const readline = require("readline");

// Ask for API Key
const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
});

const askEnv = () => {
  rl.question("🔐 Enter your GOOGLE_API_KEY: ", function (apiKey) {
    rl.close();
    fs.writeFileSync(".env", `GOOGLE_API_KEY=${apiKey}\n`);
    console.log("✅ .env file created successfully!\n");

    // Run chatbot
    execSync("chainlit run app/main.py", { stdio: "inherit" });
  });
};

console.log("🚀 Cloning HAMMAD BHAI Chatbot...");
execSync("git clone https://github.com/MUHAMMAD-HAMMAD-ZUBAIR/CHAT-BOT-2.0.git", {
  stdio: "inherit",
});
process.chdir("CHAT-BOT-2.0");

console.log("📦 Installing Python dependencies...");
execSync("pip install -r requirements.txt", { stdio: "inherit" });

askEnv();
