age=20
if age >=18:
    print("You are an adult")

Retirement_age = 65
if age >= Retirement_age:
    print("You are eligible for retirement")
else: 
    print("how many years are left until retirement")
    years_left = Retirement_age - age
    print(f"You have {years_left} years left until retirement")
def make_coffee(size):
    print("Making a", size, "coffee")

make_coffee("large")
make_coffee("small")
favourite_number = 3
print("My faourite number is", favourite_number) 
if favourite_number > 5: 
    print("That's a big number")
else:
    print("Thats a small number")
for i in range(1,4): 
    print("Loop number",i)
count = 1
while count <= 3:
    print("whilecount is", count) 
    count = count + 1
def check_answer(user_answer, correct_answer):
    if user_answer == correct_answer:
        print("correct")
    else: 
        print("incorrect")
check_answer(0.10, 0.05)
beliefs = ["I am intelligent", "I am capable", "I can Learn"]
for belief in beliefs:
    print(belief)
def check_belief(belief, evidence_count, contradiction_count):
    if evidence_count > contradiction_count:
        print(f"{belief} is supported by evidence")
    else: 
        print(f"{belief} is contradicted by evidence")
check_belief("I am wise", 5, 2)
belief_data = {"I am wise":5, "I am capable":3, "hatricks are common":1}
for belief, count in belief_data.items():
    print(belief,count)
class Belief:
    def __init__(self, name, evidence_count, contradiction_count):
        self.name = name
        self.evidence_count = evidence_count
        self.contradiction_count = contradiction_count
belief1 = Belief("I am wise", 5, 2)
belief2 = Belief("I am capable", 8,1)
print(belief1.name)
