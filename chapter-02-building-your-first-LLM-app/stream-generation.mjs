import express from "express";
import { Ollama } from "ollama";
import cors from "cors";

const app = express();

app.use(cors());
app.use(express.json());

const ollama = new Ollama();


app.post("/", async (req, res) => {
     res.type("text/plain");

     const body = req.body;
     const streamIterator = await ollama.generate({
        model: "llama3.2",
        prompt: body.question,
        stream: true
     })

     for await (const chunk of streamIterator){
        res.write(chunk.response);
     }

     res.end();
})

app.listen(9000, ()=>{
    console.log("App is running on the port 9000");
})