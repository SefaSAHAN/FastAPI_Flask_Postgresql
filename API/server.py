from fastapi import FastAPI, HTTPException , Query
from pydantic import BaseModel
import psycopg2
import uvicorn
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

conn = psycopg2.connect(dbname='flask', user='postgres', password='postgres')

class InputModel(BaseModel):
    id: int
    input: str

@app.get("/")
async def read_inputs():
    cur = conn.cursor()
    cur.execute("SELECT * FROM inputs ORDER BY id")
    inputs = cur.fetchall()
    cur.close()
    return {"inputs": inputs}

@app.post("/inputs")
async def create_input(input: InputModel):
    cur = conn.cursor()
    cur.execute("SELECT id FROM inputs WHERE id = %s", (input.id,))
    existing_input = cur.fetchone()
    if existing_input:
        raise HTTPException(status_code=400, detail="Input with this ID already exists.")
    cur.execute("INSERT INTO inputs (id, input, created_at) VALUES (%s, %s, NOW())", (input.id, input.input))
    conn.commit()
    cur.close()
    return {"message": "Input added successfully"}


@app.get("/inputs/{input}")
async def read_input(input: str):
    cur = conn.cursor()
    cur.execute(f"select * from inputs where input LIKE '{input}%' order by id")
    inputs=cur.fetchall()
    if len(inputs)>0:
        cur.close()
        return {"inputs": inputs}
    raise HTTPException(status_code=400, detail="Input not found")
    

@app.put("/inputs/{id}")
async def update_input(input: InputModel):
    cur = conn.cursor()
    cur.execute("SELECT * FROM inputs WHERE id = %s", (input.id,))
    existing_input = cur.fetchone()
    if existing_input:
        cur.execute("UPDATE inputs SET input = %s WHERE id = %s", (input.input, input.id))
        conn.commit()
        cur.close()
        return {"message": "Input updated successfully"}
    raise HTTPException(status_code=400, detail="Input with this ID not found.")
    

@app.delete("/inputs/{id}")
async def delete_input(id: int):
    cur = conn.cursor()
    cur.execute("SELECT * FROM inputs WHERE id = %s", (id,))
    existing_input = cur.fetchone()
    if existing_input:
        cur.execute("DELETE FROM inputs WHERE id = %s", (id,))
        conn.commit()
        cur.close()
        return {"message": "Input deleted successfully"}
    raise HTTPException(status_code=400, detail="Input with this ID not found.")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
