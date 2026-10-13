import express from "express";
import { Ollama } from "ollama";

const app = express();

const ollama = new Ollama();


app.get("/", async (req, res) => {
     res.type("text/plain");

     const modelResponse = await ollama.generate({
        model: "llama3.2",
        prompt: "diff between the mjs file and normal js file"
     })

     res.send(modelResponse.response);
})

app.listen(8000, ()=>{
    console.log("App is running on the port 8000")
})