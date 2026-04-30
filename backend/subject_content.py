"""
Subject-specific content generator for personalized learning
Creates different materials for Math, Science, Programming, English, and Aptitude
"""

from typing import Dict, List, Optional

# Subject-specific curriculum content
SUBJECT_CONTENT = {
    "math": {
        "topics": ["Fractions", "Algebra", "Geometry", "Statistics", "Calculus"],
        "overview": "Mathematics covers numerical reasoning, equations, shapes, and patterns.",
        "content": {
            "Fractions": {
                "explanation": "Fractions represent parts of a whole. They consist of a numerator (top) and denominator (bottom).",
                "key_points": [
                    "1/2 means 1 part out of 2 equal parts",
                    "To add fractions, find common denominator",
                    "To multiply fractions, multiply numerators and denominators",
                    "Simplify by dividing both by common factors",
                    "1/2 = 0.5 = 50%"
                ],
                "formulas": [
                    "a/b + c/d = (ad + bc)/bd",
                    "a/b × c/d = ac/bd",
                    "a/b ÷ c/d = a/b × d/c"
                ],
                "real_life": "Cooking (1/2 cup flour), sharing pizza slices, calculating discounts",
                "flashcards": [
                    {"q": "What is 1/2 + 1/4?", "a": "3/4 (convert to common denominator: 2/4 + 1/4 = 3/4)"},
                    {"q": "Simplify 4/8", "a": "1/2 (divide both by 4)"},
                    {"q": "Convert 0.75 to fraction", "a": "3/4 (0.75 = 75/100 = 3/4)"},
                    {"q": "What is 2/3 × 3/5?", "a": "6/15 = 2/5"},
                    {"q": "3/4 ÷ 1/2 = ?", "a": "3/4 × 2/1 = 6/4 = 3/2 = 1.5"},
                    {"q": "Simplify 15/20", "a": "3/4 (GCD is 5)"},
                    {"q": "1/3 + 1/3 + 1/3 = ?", "a": "1 (3/3)"},
                    {"q": "What is 5/6 - 1/6?", "a": "4/6 = 2/3"},
                    {"q": "Convert 1/5 to decimal", "a": "0.2"},
                    {"q": "What is 1/4 of 20?", "a": "5 (multiply 1/4 × 20 = 5)"},
                    {"q": "Simplify 9/12", "a": "3/4 (divide by 3)"},
                    {"q": "What is 2/5 + 1/2?", "a": "9/10 (4/10 + 5/10)"}
                ],
                "common_mistakes": ["Forgetting to find common denominator when adding", "Cross-multiplying instead of cross-canceling", "Adding denominators instead of keeping same"]
            },
            "Algebra": {
                "explanation": "Algebra uses letters (variables) to represent unknown numbers and solve equations.",
                "key_points": [
                    "Variables (x, y, z) represent unknown numbers",
                    "An equation has two equal sides",
                    "To solve, isolate the variable on one side",
                    "Use inverse operations (opposite operations)",
                    "Check your answer by substituting back"
                ],
                "formulas": [
                    "Linear equation: ax + b = c",
                    "Quadratic: ax² + bx + c = 0",
                    "Slope-intercept form: y = mx + b"
                ],
                "real_life": "Budget calculations, distance-speed problems, pricing models",
                "flashcards": [
                    {"q": "Solve: x + 5 = 12", "a": "x = 7 (subtract 5 from both sides)"},
                    {"q": "Solve: 2x = 16", "a": "x = 8 (divide both sides by 2)"},
                    {"q": "Expand: 2(x + 3)", "a": "2x + 6"},
                    {"q": "Factor: x² + 5x + 6", "a": "(x + 2)(x + 3)"},
                    {"q": "Solve: 3x - 7 = 11", "a": "x = 6 (add 7, then divide by 3)"},
                    {"q": "Combine: 2x + 3x", "a": "5x (like terms)"},
                    {"q": "Solve: x/2 = 5", "a": "x = 10 (multiply both sides by 2)"},
                    {"q": "Expand: -3(2x - 1)", "a": "-6x + 3"},
                    {"q": "Solve: 4x + 2 = 18", "a": "x = 4 (subtract 2, divide by 4)"},
                    {"q": "Factor: 2x² + 4x", "a": "2x(x + 2)"},
                    {"q": "Solve: x - 3 = 7", "a": "x = 10 (add 3 to both sides)"},
                    {"q": "What is slope in y = 2x + 3?", "a": "2 (coefficient of x)"}
                ],
                "common_mistakes": ["Forgetting to do same operation on both sides", "Not distributing correctly", "Sign errors when moving terms"]
            },
            "Geometry": {
                "explanation": "Geometry studies shapes, sizes, positions, and properties of figures.",
                "key_points": [
                    "Points, lines, and angles are basic elements",
                    "Triangles have 3 sides and angles sum to 180°",
                    "Circles have radius, diameter, and circumference",
                    "Area measures 2D space, volume measures 3D space",
                    "Pythagorean theorem: a² + b² = c²"
                ],
                "formulas": [
                    "Area of rectangle: length × width",
                    "Area of triangle: 1/2 × base × height",
                    "Area of circle: πr²",
                    "Circumference: 2πr or πd",
                    "Volume of cube: side³"
                ],
                "real_life": "Building construction, land measurement, architecture",
                "flashcards": [
                    {"q": "Area of rectangle 5m × 3m", "a": "15 m²"},
                    {"q": "Area of triangle with base 6 and height 4", "a": "12 (1/2 × 6 × 4)"},
                    {"q": "Circumference of circle with radius 5", "a": "10π ≈ 31.4"},
                    {"q": "Pythagorean theorem formula", "a": "a² + b² = c² (for right triangles)"},
                    {"q": "Area of circle with radius 3", "a": "9π ≈ 28.27"},
                    {"q": "Perimeter of square with side 4cm", "a": "16cm (4 × 4)"},
                    {"q": "Volume of cube with side 5", "a": "125 (5³)"},
                    {"q": "What are angles in a triangle?", "a": "Sum to 180°"},
                    {"q": "Diameter if radius is 7", "a": "14 (2 × radius)"},
                    {"q": "Area of trapezoid formula", "a": "1/2 × (b₁ + b₂) × h"},
                    {"q": "What is a right angle?", "a": "90 degrees"},
                    {"q": "Pentagon has how many sides?", "a": "5"}
                ],
                "common_mistakes": ["Confusing area and perimeter", "Forgetting π in circle calculations", "Not using correct formulas for different shapes"]
            }
        }
    },
    "science": {
        "topics": ["Physics", "Chemistry", "Biology", "Ecology", "Motion"],
        "overview": "Science explores the natural world through observation and experimentation.",
        "content": {
            "Physics": {
                "explanation": "Physics studies matter, energy, forces, and how they interact in the universe.",
                "key_points": [
                    "Force = mass × acceleration (F = ma)",
                    "Speed is distance/time; velocity includes direction",
                    "Acceleration is change in velocity over time",
                    "Energy cannot be created or destroyed (conservation)",
                    "Newton's laws explain motion and forces"
                ],
                "formulas": [
                    "F = ma (Force)",
                    "v = d/t (Velocity)",
                    "a = (vf - vi)/t (Acceleration)",
                    "E = mc² (Energy)",
                    "P = W/t (Power)"
                ],
                "real_life": "Car motion, falling objects, throwing a ball, electricity",
                "flashcards": [
                    {"q": "Calculate speed: 100m in 10s", "a": "10 m/s (100 ÷ 10)"},
                    {"q": "What is velocity?", "a": "Speed with direction (vector quantity)"},
                    {"q": "Newton's first law", "a": "Object in motion stays in motion unless acted upon by force"},
                    {"q": "Calculate force if m=5kg, a=10m/s²", "a": "F = 50 N (5 × 10)"},
                    {"q": "What is acceleration?", "a": "Rate of change of velocity"},
                    {"q": "SI unit of force", "a": "Newton (N)"},
                    {"q": "What is kinetic energy?", "a": "Energy of motion (1/2 mv²)"},
                    {"q": "Newton's second law formula", "a": "F = ma"},
                    {"q": "Newton's third law", "a": "Every action has equal opposite reaction"},
                    {"q": "What is weight?", "a": "Force of gravity on object (mass × g)"},
                    {"q": "Speed vs velocity difference", "a": "Speed has no direction, velocity does"},
                    {"q": "Potential energy formula", "a": "PE = mgh (mass × gravity × height)"}
                ],
                "common_mistakes": ["Confusing speed and velocity", "Forgetting that acceleration can be negative", "Using wrong formula for motion problems"]
            },
            "Chemistry": {
                "explanation": "Chemistry studies substances, their properties, reactions, and atomic structure.",
                "key_points": [
                    "Atoms are basic building blocks of matter",
                    "Electrons, protons, neutrons make up atoms",
                    "Chemical reactions rearrange atoms into new substances",
                    "Acids have pH < 7, bases have pH > 7",
                    "Periodic table organizes elements by properties"
                ],
                "formulas": [
                    "H₂O = water (hydrogen + oxygen)",
                    "NaCl = salt (sodium + chlorine)",
                    "CO₂ = carbon dioxide",
                    "pH = -log[H+]",
                    "Molarity = moles/liters"
                ],
                "real_life": "Water treatment, medicine, cooking, batteries, plastic production",
                "flashcards": [
                    {"q": "What is H₂O?", "a": "Water - made of 2 hydrogen and 1 oxygen atom"},
                    {"q": "What is an atom?", "a": "Smallest unit of an element that retains its properties"},
                    {"q": "Acid or base: pH 3", "a": "Acid (pH < 7)"},
                    {"q": "Combustion of methane", "a": "CH₄ + 2O₂ → CO₂ + 2H₂O"},
                    {"q": "What is oxidation?", "a": "Loss of electrons or gain of oxygen"},
                    {"q": "Parts of an atom", "a": "Protons (positive), neutrons (neutral), electrons (negative)"},
                    {"q": "What is NaCl?", "a": "Sodium chloride (table salt)"},
                    {"q": "Acid or base: pH 11", "a": "Base (pH > 7)"},
                    {"q": "What is reduction?", "a": "Gain of electrons or loss of oxygen"},
                    {"q": "Name CO₂", "a": "Carbon dioxide"},
                    {"q": "What is pH 7?", "a": "Neutral (neither acidic nor basic)"},
                    {"q": "What is a chemical reaction?", "a": "Rearrangement of atoms to form new substances"}
                ],
                "common_mistakes": ["Mixing up acids and bases", "Not balancing chemical equations", "Forgetting units in calculations"]
            },
            "Biology": {
                "explanation": "Biology is the study of living organisms and their interactions.",
                "key_points": [
                    "Cell is the basic unit of life",
                    "DNA carries genetic information",
                    "Photosynthesis converts light into energy",
                    "Mitosis is cell division for growth",
                    "Evolution is change through natural selection"
                ],
                "formulas": [
                    "Photosynthesis: 6CO₂ + 6H₂O + light → C₆H₁₂O₆ + 6O₂",
                    "Cellular respiration: C₆H₁₂O₆ + 6O₂ → 6CO₂ + 6H₂O + energy",
                    "DNA structure: double helix with base pairs"
                ],
                "real_life": "Health, genetics, agriculture, disease prevention, nutrition",
                "flashcards": [
                    {"q": "What does mitochondria do?", "a": "Produces energy (ATP) for the cell"},
                    {"q": "What is photosynthesis?", "a": "Process where plants convert light energy to chemical energy"},
                    {"q": "DNA stands for?", "a": "Deoxyribonucleic acid"},
                    {"q": "What is a gene?", "a": "Section of DNA that codes for a protein"},
                    {"q": "Cell organelle that controls cell", "a": "Nucleus"},
                    {"q": "What does chloroplast do?", "a": "Photosynthesis - converts light to chemical energy"},
                    {"q": "What is cellular respiration?", "a": "Breakdown of glucose to produce ATP (energy)"},
                    {"q": "What is mitosis?", "a": "Cell division producing 2 identical daughter cells"},
                    {"q": "What is meiosis?", "a": "Cell division producing 4 sex cells (gametes)"},
                    {"q": "What do ribosomes do?", "a": "Manufacture proteins based on DNA instructions"},
                    {"q": "Three base pairs code for?", "a": "One amino acid (codon)"},
                    {"q": "What is evolution?", "a": "Change in living things through natural selection"}
                ],
                "common_mistakes": ["Confusing photosynthesis and respiration", "Not understanding DNA-protein relationship", "Forgetting plants also respire"]
            }
        }
    },
    "programming": {
        "topics": ["Loops", "Variables", "Functions", "Conditionals", "Arrays"],
        "overview": "Programming teaches logical thinking and how to write code to solve problems.",
        "content": {
            "Loops": {
                "explanation": "Loops repeat code blocks automatically - essential for processing large amounts of data.",
                "key_points": [
                    "For loop: repeat fixed number of times",
                    "While loop: repeat while condition is true",
                    "Do-while: execute at least once, then check",
                    "Break exits loop, continue skips to next iteration",
                    "Nested loops: loop inside a loop"
                ],
                "formulas": [
                    "for i in range(n): # 0 to n-1",
                    "while condition: # repeat while true",
                    "for item in list: # iterate through list",
                    "break # exit loop",
                    "continue # skip to next iteration"
                ],
                "real_life": "Processing arrays of data, game loops, animations, data analysis",
                "flashcards": [
                    {"q": "Output: for i in range(3): print(i)", "a": "0\\n1\\n2 (range(3) gives 0,1,2)"},
                    {"q": "What does break do?", "a": "Exits the loop immediately"},
                    {"q": "What does continue do?", "a": "Skips current iteration, goes to next"},
                    {"q": "for i in range(1,4): print(i)", "a": "1\\n2\\n3 (start=1, stop=4, not inclusive)"},
                    {"q": "How to loop 5 times?", "a": "for i in range(5): or for i in range(0,5):"},
                    {"q": "What is infinite loop?", "a": "Loop that never ends (while True:)"},
                    {"q": "for i in range(2, 8, 2)", "a": "Prints 2, 4, 6 (start=2, stop=8, step=2)"},
                    {"q": "for item in [1,2,3]", "a": "Iterates through list items"},
                    {"q": "Nested loop definition", "a": "Loop inside another loop"},
                    {"q": "while condition - when stops?", "a": "When condition becomes False"},
                    {"q": "What loop do-while always does?", "a": "Executes at least once before checking condition"},
                    {"q": "Purpose of loops", "a": "Repeat code without rewriting it"}
                ],
                "common_mistakes": ["Forgetting range() goes 0 to n-1, not including n", "Infinite loops with while", "Off-by-one errors in ranges"]
            },
            "Variables": {
                "explanation": "Variables store data values that your program can use and modify.",
                "key_points": [
                    "Variable = storage container for data",
                    "Data types: int, float, string, boolean",
                    "Variables can change value",
                    "Naming: descriptive, no spaces, case-sensitive",
                    "Memory allocated when variable created"
                ],
                "formulas": [
                    "x = 5 # assign value",
                    "name = 'John' # string",
                    "is_active = True # boolean",
                    "price = 9.99 # float",
                    "x = x + 1 # update variable"
                ],
                "real_life": "Storing user input, keeping score in games, storing calculations",
                "flashcards": [
                    {"q": "What is a variable?", "a": "Named storage location that holds a value"},
                    {"q": "Which is valid variable name?", "a": "user_age (not '2user' or 'user age')"},
                    {"q": "int vs float difference", "a": "int is whole number, float has decimals"},
                    {"q": "What is x after: x=5; x=x+2", "a": "x = 7"},
                    {"q": "String vs integer", "a": "'5' is string, 5 is integer"},
                    {"q": "Boolean data type holds", "a": "True or False"},
                    {"q": "Variable naming rules", "a": "Start with letter/underscore, no spaces, case-sensitive"},
                    {"q": "Is 'class' a valid variable name?", "a": "No - it's a Python keyword"},
                    {"q": "Type of: age = 25", "a": "Integer (int)"},
                    {"q": "Type of: name = 'Alex'", "a": "String (str)"},
                    {"q": "Type of: is_active = True", "a": "Boolean (bool)"},
                    {"q": "What is scope?", "a": "Region where a variable is accessible"}
                ],
                "common_mistakes": ["Using variable before declaring", "Forgetting quotes for strings", "Case sensitivity issues"]
            },
            "Functions": {
                "explanation": "Functions are reusable blocks of code that perform specific tasks.",
                "key_points": [
                    "Function = reusable block of code",
                    "Parameters are inputs to function",
                    "Return statement sends result back",
                    "Function call executes the code",
                    "Scope: variables inside function are local"
                ],
                "formulas": [
                    "def function_name(param1, param2):",
                    "    return result",
                    "function_name(arg1, arg2) # call function",
                    "def greet(name): print('Hi ' + name)",
                    "x = function_name() # store return value"
                ],
                "real_life": "Reusing code, organizing programs, math operations, game mechanics",
                "flashcards": [
                    {"q": "What is a function?", "a": "Reusable block of code that performs a task"},
                    {"q": "What does return do?", "a": "Sends result back to caller and ends function"},
                    {"q": "Parameter vs argument", "a": "Parameter in definition, argument in call"},
                    {"q": "def add(a,b): return a+b; print(add(3,4))", "a": "Prints 7"},
                    {"q": "Local vs global variable", "a": "Local inside function only, global accessible everywhere"},
                    {"q": "Function without return sends", "a": "None"},
                    {"q": "Multiple return values?", "a": "Yes, use tuple: return x, y"},
                    {"q": "Can function call itself?", "a": "Yes - recursion"},
                    {"q": "Default parameter: def greet(name='Friend')", "a": "If no argument, uses 'Friend'"},
                    {"q": "Function syntax requirement", "a": "Colon after def line"},
                    {"q": "What is recursion?", "a": "Function calling itself (must have base case)"},
                    {"q": "Why use functions?", "a": "Reusability, organize code, readability"}
                ],
                "common_mistakes": ["Forgetting colon after def", "Not returning value when needed", "Calling function before defining it"]
            }
        }
    },
    "english": {
        "topics": ["Grammar", "Comprehension", "Vocabulary", "Writing", "Literature"],
        "overview": "English develops reading, writing, speaking, and critical thinking skills.",
        "content": {
            "Grammar": {
                "explanation": "Grammar is the system and structure of a language.",
                "key_points": [
                    "Subject performs action, verb is the action",
                    "Every sentence needs subject and verb",
                    "Tense shows when action happens",
                    "Punctuation marks end thoughts and add clarity",
                    "Parts of speech: noun, verb, adjective, adverb, preposition"
                ],
                "formulas": [
                    "Subject + Verb + Object = basic sentence",
                    "Present: I go, He goes",
                    "Past: I went, I was",
                    "Future: I will go, I am going to go",
                    "Comma, period, question mark, exclamation"
                ],
                "real_life": "Writing emails, essays, messages, professional documents",
                "flashcards": [
                    {"q": "Correct: 'She go' or 'She goes'?", "a": "'She goes' (third person singular needs -s)"},
                    {"q": "What is a noun?", "a": "A person, place, thing, or idea (dog, tree, happiness)"},
                    {"q": "What is a verb?", "a": "Action word or state of being (run, is, think)"},
                    {"q": "Tense of: 'I have finished'", "a": "Present perfect (past action relevant now)"},
                    {"q": "Correct: 'between you and I' or 'between you and me'?", "a": "'between you and me' (me is object of preposition)"},
                    {"q": "What is an adjective?", "a": "Word that describes a noun (big, red, happy)"},
                    {"q": "What is an adverb?", "a": "Word that describes verb/adjective (quickly, very)"},
                    {"q": "Simple past of 'go'", "a": "went (irregular verb)"},
                    {"q": "Collective noun example", "a": "Herd, flock, group (singular noun for many)"},
                    {"q": "What is a preposition?", "a": "Shows relationship (in, on, under, between)"},
                    {"q": "Subject-verb agreement means", "a": "Subject and verb must match in number"},
                    {"q": "What is a clause?", "a": "Group of words with subject and verb"}
                ],
                "common_mistakes": ["Subject-verb disagreement", "Wrong tense use", "Comma splices", "Misplaced modifiers"]
            },
            "Comprehension": {
                "explanation": "Reading comprehension is understanding and analyzing written text.",
                "key_points": [
                    "Read for main idea, supporting details, and purpose",
                    "Infer meaning from context",
                    "Distinguish fact from opinion",
                    "Identify author's tone and bias",
                    "Make connections to prior knowledge"
                ],
                "formulas": [
                    "Main idea = what text is mostly about",
                    "Supporting details = facts that explain main idea",
                    "Inference = conclusion based on evidence",
                    "Fact = can be proven true",
                    "Opinion = personal belief"
                ],
                "real_life": "Reading news, understanding instructions, analyzing articles, academic studies",
                "flashcards": [
                    {"q": "What is the main idea?", "a": "The central point or primary message of the text"},
                    {"q": "What is an inference?", "a": "Logical conclusion based on facts and evidence"},
                    {"q": "Fact or Opinion: 'Cats are animals'", "a": "Fact (can be proven)"},
                    {"q": "Author's tone = ?", "a": "The attitude or feeling the author expresses"},
                    {"q": "Context clues help", "a": "Understand word meanings from surrounding text"},
                    {"q": "What are supporting details?", "a": "Facts that explain and support the main idea"},
                    {"q": "What is summarizing?", "a": "Briefly stating main points in your own words"},
                    {"q": "Author's purpose could be", "a": "Entertain, inform, persuade, or educate"},
                    {"q": "What is author's bias?", "a": "Author's preference or prejudice"},
                    {"q": "Distinguish fact from opinion:", "a": "Fact: provable, Opinion: belief or judgment"},
                    {"q": "What is text structure?", "a": "How author organizes ideas (sequence, cause-effect)"},
                    {"q": "What is theme?", "a": "Central message or lesson of the story"}
                ],
                "common_mistakes": ["Confusing main idea with details", "Making assumptions without evidence", "Ignoring context"]
            },
            "Vocabulary": {
                "explanation": "Vocabulary is the collection of words you know and can use effectively.",
                "key_points": [
                    "Synonyms = words with similar meaning",
                    "Antonyms = words with opposite meaning",
                    "Prefixes/suffixes change word meaning",
                    "Word roots help understand new words",
                    "Context helps determine meaning"
                ],
                "formulas": [
                    "Prefix (before) + Root + Suffix (after) = word",
                    "un- = not, re- = again, -ing = doing",
                    "-tion = action/state, -ous = full of",
                    "Synonym example: happy = joyful",
                    "Antonym example: big ≠ small"
                ],
                "real_life": "Speaking fluently, writing clearly, understanding media, academic success",
                "flashcards": [
                    {"q": "Synonym for 'big'", "a": "Large, huge, enormous, vast"},
                    {"q": "Antonym for 'happy'", "a": "Sad, unhappy, miserable"},
                    {"q": "Prefix 'un-' means", "a": "Not or opposite (unhappy, unclear)"},
                    {"q": "Suffix '-tion' indicates", "a": "An action or state (creation, attention)"},
                    {"q": "What is 'benevolent'?", "a": "Kind, generous, charitable"},
                    {"q": "Prefix 're-' means", "a": "Again or back (redo, return)"},
                    {"q": "Suffix '-ing' shows", "a": "Action in progress (running, jumping)"},
                    {"q": "Prefix 'dis-' means", "a": "Not, opposite, or reverse (disagree, dislike)"},
                    {"q": "Suffix '-ful' means", "a": "Full of (beautiful, helpful, joyful)"},
                    {"q": "Suffix '-ous' means", "a": "Full of or characterized by (dangerous, famous)"},
                    {"q": "Root 'bio' means", "a": "Life (biology, biography)"},
                    {"q": "Root 'port' means", "a": "Carry (transport, import, export)"}
                ],
                "common_mistakes": ["Confusing similar-looking words", "Not learning word roots", "Ignoring context when guessing meaning"]
            }
        }
    },
    "aptitude": {
        "topics": ["Reasoning", "Logic", "Problem-Solving", "Patterns", "Puzzles"],
        "overview": "Aptitude tests measure reasoning ability and problem-solving skills.",
        "content": {
            "Reasoning": {
                "explanation": "Reasoning is using logic to think through problems and reach conclusions.",
                "key_points": [
                    "Logical reasoning follows rules and patterns",
                    "Deductive: general rule → specific case",
                    "Inductive: specific cases → general rule",
                    "Analogies: identify relationships between pairs",
                    "Syllogisms: if A=B and B=C, then A=C"
                ],
                "formulas": [
                    "Deductive: All humans are mortal, John is human → John is mortal",
                    "Inductive: 2+2=4, 3+3=6, 4+4=8 → odd+odd=even",
                    "Analogy: Cat is to meow as Dog is to bark",
                    "Series: 2,4,6,8,? → 10 (pattern: +2)"
                ],
                "real_life": "Interviews, competitive exams, decision making, analytical thinking",
                "flashcards": [
                    {"q": "All cats are animals. Fluffy is a cat. Fluffy is?", "a": "An animal (deductive reasoning)"},
                    {"q": "2 is even, 4 is even, 6 is even. Pattern?", "a": "All positive even numbers (inductive reasoning)"},
                    {"q": "Eye is to see as Ear is to ?", "a": "Hear (analogies find relationships)"},
                    {"q": "Find next: 1,4,9,16,?", "a": "25 (pattern: 1²,2²,3²,4²,5²)"},
                    {"q": "If A>B and B>C, then A>C. This is?", "a": "Logical deduction (transitive property)"},
                    {"q": "Find next: 2,4,6,8,?", "a": "10 (arithmetic sequence: +2)"},
                    {"q": "Deduction vs Induction", "a": "Deduction: specific from general. Induction: general from specific"},
                    {"q": "What is a syllogism?", "a": "Three-part logical argument (2 premises, 1 conclusion)"},
                    {"q": "Hand is to glove as Foot is to", "a": "Shoe (function analogy)"},
                    {"q": "Find next: 1,1,2,3,5,8,?", "a": "13 (Fibonacci sequence: each = sum of previous two)"},
                    {"q": "What is lateral thinking?", "a": "Solving problems from fresh angle"},
                    {"q": "Pattern: 3,6,12,24,?", "a": "48 (each multiplies by 2)"}
                ],
                "common_mistakes": ["Assuming without verifying", "Mixing up deductive and inductive", "Not identifying the correct relationship"]
            },
            "Logic": {
                "explanation": "Logic is the study of reasoning - distinguishing valid from invalid arguments.",
                "key_points": [
                    "Valid argument: conclusion must be true if premises are true",
                    "Invalid argument: conclusion may not follow from premises",
                    "Premises are given facts, conclusion is derived",
                    "Identify hidden assumptions",
                    "Check for logical fallacies"
                ],
                "formulas": [
                    "P1: A implies B",
                    "P2: A is true",
                    "C: Therefore B is true",
                    "Logical operators: AND, OR, NOT, IF-THEN",
                    "Truth table for logical operations"
                ],
                "real_life": "Debates, programming logic, legal arguments, critical analysis",
                "flashcards": [
                    {"q": "If it rains, grass is wet. Grass is wet. Does it rain?", "a": "Not necessarily (logical fallacy - affirming consequent)"},
                    {"q": "Valid or invalid: All birds fly. Penguins are birds. Penguins fly.", "a": "Invalid - penguins don't fly (logical form valid but false premise)"},
                    {"q": "What is a fallacy?", "a": "Logical error in reasoning or invalid argument"},
                    {"q": "AND operator means", "a": "Both conditions must be true"},
                    {"q": "OR operator means", "a": "At least one condition must be true"},
                    {"q": "NOT operator means", "a": "Negation or opposite"},
                    {"q": "Correlation vs Causation", "a": "Correlation: happen together. Causation: one causes other"},
                    {"q": "Ad hominem fallacy is", "a": "Attacking person instead of their argument"},
                    {"q": "Begging the question means", "a": "Assuming conclusion in premise (circular reasoning)"},
                    {"q": "Straw man fallacy", "a": "Misrepresenting opponent's argument"},
                    {"q": "What is a premise?", "a": "Given fact or statement in an argument"},
                    {"q": "Modus ponens rule", "a": "If A implies B and A is true, then B is true"}
                ],
                "common_mistakes": ["Confusing correlation with causation", "Circular reasoning", "Ad hominem attacks"]
            },
            "Problem-Solving": {
                "explanation": "Problem-solving is a systematic approach to finding solutions.",
                "key_points": [
                    "Understand the problem completely",
                    "Identify what you know and don't know",
                    "Consider multiple approaches",
                    "Plan before solving",
                    "Check and verify your answer"
                ],
                "formulas": [
                    "Steps: Understand → Plan → Execute → Verify",
                    "Breakdown complex problems into steps",
                    "Use examples or diagrams",
                    "Eliminate impossible options",
                    "Try simpler versions first"
                ],
                "real_life": "Math problems, puzzles, real-world challenges, coding issues",
                "flashcards": [
                    {"q": "First step in problem-solving", "a": "Understand the problem completely"},
                    {"q": "If direct approach doesn't work, try?", "a": "Work backwards, try examples, draw diagram"},
                    {"q": "What helps verify solution?", "a": "Check by substituting back or testing"},
                    {"q": "Complex problem strategy", "a": "Break into smaller, manageable parts"},
                    {"q": "After solving, do?", "a": "Review solution for errors and logic"},
                    {"q": "What is brute force?", "a": "Try all possibilities until finding answer"},
                    {"q": "What is working backwards?", "a": "Start from desired result, work to initial state"},
                    {"q": "Guess and check strategy", "a": "Make reasonable guess, test, refine"},
                    {"q": "What is trial and error?", "a": "Trying different solutions until success"},
                    {"q": "What is pattern recognition?", "a": "Identifying similarities to solve problems"},
                    {"q": "Visualization helps by", "a": "Creating mental or physical picture of problem"},
                    {"q": "Key to complex problems", "a": "Divide into simpler subproblems"}
                ],
                "common_mistakes": ["Jumping to solving without understanding", "Not checking work", "Giving up too quickly"]
            }
        }
    }
}

def get_subject_content(subject: str) -> Dict:
    """Get complete content for a subject"""
    subject_lower = subject.lower()
    
    for subj_key, subj_data in SUBJECT_CONTENT.items():
        if subject_lower.startswith(subj_key) or subj_key in subject_lower.lower():
            return subj_data
    
    # Return generic content if subject not found
    return {
        "topics": ["General", "Basics", "Advanced", "Practice"],
        "overview": f"Learning content for {subject}",
        "content": {}
    }

def get_topic_content(subject: str, topic: str) -> Dict:
    """Get content for a specific topic within a subject"""
    subject_data = get_subject_content(subject)
    
    if "content" in subject_data and topic in subject_data["content"]:
        return subject_data["content"][topic]
    
    return {
        "explanation": f"Learn about {topic} in {subject}",
        "key_points": [f"Key point about {topic}"],
        "real_life": f"Real-world applications of {topic}",
        "flashcards": [
            {"q": f"What is {topic}?", "a": f"{topic} is an important concept in {subject}"}
        ]
    }

def generate_subject_flashcards(subject: str, limit: int = 10) -> List[Dict]:
    """Generate flashcards for a subject"""
    subject_data = get_subject_content(subject)
    flashcards = []
    
    if "content" in subject_data:
        for topic, content in subject_data["content"].items():
            if "flashcards" in content:
                flashcards.extend(content["flashcards"])
    
    return flashcards[:limit]

def generate_subject_revision(subject: str, topic: Optional[str] = None) -> Dict:
    """Generate revision guide with key points and common mistakes"""
    subject_data = get_subject_content(subject)
    
    revision = {
        "important_topics": subject_data.get("topics", []),
        "key_points": [],
        "common_mistakes": [],
        "quick_tips": []
    }
    
    if "content" in subject_data:
        topics_to_cover = [topic] if topic and topic in subject_data["content"] else list(subject_data["content"].keys())
        
        for tp in topics_to_cover:
            if tp in subject_data["content"]:
                content = subject_data["content"][tp]
                revision["key_points"].extend(content.get("key_points", [])[:3])
                revision["common_mistakes"].extend(content.get("common_mistakes", [])[:2])
    
    # Add quick tips based on subject
    tips_by_subject = {
        "math": ["Practice regularly", "Show all steps", "Check your work"],
        "science": ["Do experiments", "Understand concepts", "Connect to real world"],
        "programming": ["Write code daily", "Debug systematically", "Refactor often"],
        "english": ["Read daily", "Practice writing", "Learn roots and prefixes"],
        "aptitude": ["Think logically", "Practice patterns", "Manage time wisely"]
    }
    
    subject_lower = subject.lower()
    for key in tips_by_subject:
        if key in subject_lower:
            revision["quick_tips"] = tips_by_subject[key]
            break
    
    return revision

def generate_subject_notes(subject: str) -> Dict:
    """Generate comprehensive notes for a subject"""
    subject_data = get_subject_content(subject)
    
    notes = {
        "subject": subject,
        "overview": subject_data.get("overview", ""),
        "topics": [],
        "key_formulas": []
    }
    
    if "content" in subject_data:
        for topic_name, content in subject_data["content"].items():
            notes["topics"].append({
                "name": topic_name,
                "explanation": content.get("explanation", ""),
                "key_points": content.get("key_points", [])[:5],
                "formulas": content.get("formulas", [])[:3]
            })
            notes["key_formulas"].extend(content.get("formulas", [])[:2])
    
    return notes
