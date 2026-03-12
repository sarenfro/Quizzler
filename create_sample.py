"""Run this once to generate a sample quiz.xlsx"""
import openpyxl

wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Quiz"

headers = ["Question", "Option A", "Option B", "Option C", "Option D", "Right Answer"]
ws.append(headers)

questions = [
    ["What is the capital of France?", "Berlin", "Madrid", "Paris", "Rome", "C"],
    ["Which planet is closest to the Sun?", "Venus", "Earth", "Mars", "Mercury", "D"],
    ["What is 7 x 8?", "54", "56", "58", "64", "B"],
    ["Who wrote Romeo and Juliet?", "Charles Dickens", "William Shakespeare", "Jane Austen", "Mark Twain", "B"],
    ["What is the chemical symbol for water?", "CO2", "O2", "H2O", "NaCl", "C"],
    ["How many sides does a hexagon have?", "5", "6", "7", "8", "B"],
    ["What is the largest ocean on Earth?", "Atlantic", "Indian", "Arctic", "Pacific", "D"],
    ["Which gas do plants absorb from the atmosphere?", "Oxygen", "Nitrogen", "Carbon Dioxide", "Hydrogen", "C"],
]

for q in questions:
    ws.append(q)

wb.save("quiz.xlsx")
print("quiz.xlsx created successfully.")
