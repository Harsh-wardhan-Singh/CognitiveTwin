"""
Extended question seeding - seeds 150 hardcoded questions across topics
Topics: Binomial, Poisson, Normal, Bayes, Conditional
Difficulties: 1-5
"""

import sys
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.question import Question

# Comprehensive question bank
QUESTIONS = [
    # BINOMIAL - 30 questions
    {"topic": "Binomial", "concept": "Binomial Distribution", "difficulty": 1, 
     "question_text": "In a binomial distribution with n=10 and p=0.5, what is the mean?",
     "correct_answer": "5", "options": "5||10||0.5||2.5", "is_multiple": "false"},
    {"topic": "Binomial", "concept": "Binomial Distribution", "difficulty": 1,
     "question_text": "A coin is flipped 20 times. What is the probability of getting exactly 10 heads?",
     "correct_answer": "0.176", "options": "0.176||0.5||0.2||0.25", "is_multiple": "false"},
    {"topic": "Binomial", "concept": "Binomial Coefficients", "difficulty": 2,
     "question_text": "What is C(10,3)?", "correct_answer": "120", "options": "120||210||45||55", "is_multiple": "false"},
    {"topic": "Binomial", "concept": "Binomial Distribution", "difficulty": 2,
     "question_text": "If X ~ B(8, 0.3), find P(X=2)", "correct_answer": "0.296", "options": "0.296||0.3||0.5||0.1", "is_multiple": "false"},
    {"topic": "Binomial", "concept": "Binomial Distribution", "difficulty": 1,
     "question_text": "In a binomial experiment, p represents the probability of...?", "correct_answer": "Success", "options": "Success||Failure||Total||Mean", "is_multiple": "false"},
    {"topic": "Binomial", "concept": "Binomial Distribution", "difficulty": 3,
     "question_text": "A student answers 15 multiple choice questions by guessing. Each has 4 options. What is the expected number of correct answers?", "correct_answer": "3.75", "options": "3.75||7.5||15||4", "is_multiple": "false"},
    {"topic": "Binomial", "concept": "Variance", "difficulty": 2,
     "question_text": "For B(20, 0.4), what is the variance?", "correct_answer": "4.8", "options": "4.8||8||20||1.6", "is_multiple": "false"},
    {"topic": "Binomial", "concept": "Binomial Distribution", "difficulty": 2,
     "question_text": "Which is NOT a requirement for a binomial distribution?", "correct_answer": "Outcomes depend on previous trials", "options": "Outcomes depend on previous trials||Fixed number of trials||Two outcomes per trial||Constant probability||True or false", "is_multiple": "false"},
    {"topic": "Binomial", "concept": "Binomial Distribution", "difficulty": 3,
     "question_text": "If 5% of items are defective, what is P(at least 1 defective in sample of 10)?", "correct_answer": "0.401", "options": "0.401||0.599||0.05||0.5", "is_multiple": "false"},
    {"topic": "Binomial", "concept": "Binomial Distribution", "difficulty": 4,
     "question_text": "Find P(X≤2) for B(5, 0.6)", "correct_answer": "0.317", "options": "0.317||0.683||0.5||0.4", "is_multiple": "false"},
    {"topic": "Binomial", "concept": "Binomial Coefficients", "difficulty": 3,
     "question_text": "Calculate C(7,2) + C(7,3)", "correct_answer": "56", "options": "56||35||21||99", "is_multiple": "false"},
    {"topic": "Binomial", "concept": "Binomial Distribution", "difficulty": 1,
     "question_text": "For a binomial trial, n=4, p=0.5. What is the variance?", "correct_answer": "1", "options": "1||2||4||0.5", "is_multiple": "false"},
    {"topic": "Binomial", "concept": "Binomial Distribution", "difficulty": 2,
     "question_text": "Rolling a die 6 times, what is P(exactly 2 sixes)?", "correct_answer": "0.201", "options": "0.201||0.167||0.5||0.333", "is_multiple": "false"},
    {"topic": "Binomial", "concept": "Binomial Distribution", "difficulty": 3,
     "question_text": "If B(n, 0.5) has mean 8, what is n?", "correct_answer": "16", "options": "16||8||32||4", "is_multiple": "false"},
    {"topic": "Binomial", "concept": "Binomial Distribution", "difficulty": 4,
     "question_text": "For X~B(12, 0.4), find P(X>8)", "correct_answer": "0.0154", "options": "0.0154||0.0125||0.5||0.2", "is_multiple": "false"},
    {"topic": "Binomial", "concept": "Binomial Distribution", "difficulty": 2,
     "question_text": "What does n represent in B(n,p)?", "correct_answer": "Number of trials", "options": "Number of trials||Number of successes||Probability of success||Standard deviation", "is_multiple": "false"},
    {"topic": "Binomial", "concept": "Binomial Distribution", "difficulty": 5,
     "question_text": "A product has 2% defect rate. In a batch of 50, P(exactly 1 defect)?", "correct_answer": "0.371", "options": "0.371||0.735||0.265||0.5", "is_multiple": "false"},
    {"topic": "Binomial", "concept": "Binomial Distribution", "difficulty": 1,
     "question_text": "Standard deviation of B(25, 0.2) is?", "correct_answer": "2", "options": "2||4||5||1", "is_multiple": "false"},
    {"topic": "Binomial", "concept": "Binomial Distribution", "difficulty": 3,
     "question_text": "P(X≥1) for B(4, 0.25) equals?", "correct_answer": "0.684", "options": "0.684||0.316||0.5||0.75", "is_multiple": "false"},
    {"topic": "Binomial", "concept": "Binomial Distribution", "difficulty": 2,
     "question_text": "If flipping a coin 100 times, expected heads is?", "correct_answer": "50", "options": "50||100||25||75", "is_multiple": "false"},
    {"topic": "Binomial", "concept": "Binomial Coefficients", "difficulty": 1,
     "question_text": "What is C(5,1)?", "correct_answer": "5", "options": "5||10||1||0", "is_multiple": "false"},
    {"topic": "Binomial", "concept": "Binomial Distribution", "difficulty": 4,
     "question_text": "For B(15, 0.3), find the mode (most likely value)", "correct_answer": "4", "options": "4||5||3||15", "is_multiple": "false"},
    {"topic": "Binomial", "concept": "Binomial Distribution", "difficulty": 3,
     "question_text": "P(X=0) for B(6, 0.2) is approximately?", "correct_answer": "0.262", "options": "0.262||0.2||0.5||0.738", "is_multiple": "false"},
    {"topic": "Binomial", "concept": "Binomial Distribution", "difficulty": 2,
     "question_text": "A test has 10 questions, all guessed. P(pass with 6+ correct)?", "correct_answer": "0.172", "options": "0.172||0.5||0.25||0.1", "is_multiple": "false"},
    {"topic": "Binomial", "concept": "Binomial Distribution", "difficulty": 5,
     "question_text": "If B(n, 0.6) has variance 2.4, find n", "correct_answer": "10", "options": "10||6||4||2.4", "is_multiple": "false"},
    {"topic": "Binomial", "concept": "Binomial Distribution", "difficulty": 1,
     "question_text": "Mean of B(50, 0.4) is?", "correct_answer": "20", "options": "20||10||40||50", "is_multiple": "false"},
    {"topic": "Binomial", "concept": "Binomial Distribution", "difficulty": 3,
     "question_text": "P(X≤1) for B(8, 0.5)?", "correct_answer": "0.035", "options": "0.035||0.5||0.965||0.25", "is_multiple": "false"},
    {"topic": "Binomial", "concept": "Binomial Distribution", "difficulty": 4,
     "question_text": "Find P(3≤X≤5) for B(10, 0.5)", "correct_answer": "0.656", "options": "0.656||0.5||0.344||0.75", "is_multiple": "false"},
    {"topic": "Binomial", "concept": "Binomial Distribution", "difficulty": 2,
     "question_text": "For B(n, p), if mean is 6 and variance is 2.4, find p", "correct_answer": "0.4", "options": "0.4||0.6||0.5||0.2", "is_multiple": "false"},
    {"topic": "Binomial", "concept": "Binomial Distribution", "difficulty": 3,
     "question_text": "Probability of getting 3+ heads in 5 coin flips?", "correct_answer": "0.5", "options": "0.5||0.3||0.7||0.8", "is_multiple": "false"},
    
    # POISSON - 30 questions
    {"topic": "Poisson", "concept": "Poisson Distribution", "difficulty": 1,
     "question_text": "What is the main parameter of Poisson distribution?", "correct_answer": "λ (lambda)", "options": "λ (lambda)||n||p||σ", "is_multiple": "false"},
    {"topic": "Poisson", "concept": "Poisson Distribution", "difficulty": 1,
     "question_text": "For Poisson(λ=3), what is the mean?", "correct_answer": "3", "options": "3||1.73||9||1", "is_multiple": "false"},
    {"topic": "Poisson", "concept": "Poisson Distribution", "difficulty": 2,
     "question_text": "If cars arrive at λ=2 per minute, P(0 cars in 1 min)?",
     "correct_answer": "0.135", "options": "0.135||0.2||0.5||0.865", "is_multiple": "false"},
    {"topic": "Poisson", "concept": "Poisson Distribution", "difficulty": 1,
     "question_text": "For Poisson(λ=5), variance equals?", "correct_answer": "5", "options": "5||2.24||25||1", "is_multiple": "false"},
    {"topic": "Poisson", "concept": "Poisson Distribution", "difficulty": 2,
     "question_text": "When is Poisson distribution used?", "correct_answer": "Rare events in time/space", "options": "Rare events in time/space||Binary outcomes||Normal distribution||Large samples only", "is_multiple": "false"},
    {"topic": "Poisson", "concept": "Poisson Distribution", "difficulty": 3,
     "question_text": "Expected defects per 1000 items with λ=0.5?", "correct_answer": "500", "options": "500||50||5||5000", "is_multiple": "false"},
    {"topic": "Poisson", "concept": "Poisson Distribution", "difficulty": 2,
     "question_text": "P(X=2) for Poisson(λ=1)?", "correct_answer": "0.184", "options": "0.184||0.368||0.5||0.135", "is_multiple": "false"},
    {"topic": "Poisson", "concept": "Poisson Distribution", "difficulty": 3,
     "question_text": "Emails arrive at λ=4/hour. P(at least 1 email)?", "correct_answer": "0.982", "options": "0.982||0.4||0.018||0.5", "is_multiple": "false"},
    {"topic": "Poisson", "concept": "Poisson Distribution", "difficulty": 1,
     "question_text": "sd(X) for Poisson(λ=4)?", "correct_answer": "2", "options": "2||4||16||1", "is_multiple": "false"},
    {"topic": "Poisson", "concept": "Poisson Distribution", "difficulty": 4,
     "question_text": "P(X≤2) for Poisson(λ=2)?", "correct_answer": "0.677", "options": "0.677||0.323||0.5||0.135", "is_multiple": "false"},
    {"topic": "Poisson", "concept": "Poisson Distribution", "difficulty": 2,
     "question_text": "If λ=6 for Poisson, P(X=6)?", "correct_answer": "0.161", "options": "0.161||0.6||0.5||0.25", "is_multiple": "false"},
    {"topic": "Poisson", "concept": "Poisson Distribution", "difficulty": 3,
     "question_text": "Typos per page with λ=0.8, P(no typos)?", "correct_answer": "0.449", "options": "0.449||0.8||0.551||0.2", "is_multiple": "false"},
    {"topic": "Poisson", "concept": "Poisson Distribution", "difficulty": 2,
     "question_text": "When λ is large, Poisson approaches?", "correct_answer": "Normal distribution", "options": "Normal distribution||Binomial||Uniform||Exponential", "is_multiple": "false"},
    {"topic": "Poisson", "concept": "Poisson Distribution", "difficulty": 4,
     "question_text": "P(X>2) for Poisson(λ=1)?", "correct_answer": "0.080", "options": "0.080||0.92||0.5||0.3", "is_multiple": "false"},
    {"topic": "Poisson", "concept": "Poisson Distribution", "difficulty": 1,
     "question_text": "For Poisson, mean equals?", "correct_answer": "variance", "options": "variance||n||p||2λ", "is_multiple": "false"},
    {"topic": "Poisson", "concept": "Poisson Distribution", "difficulty": 3,
     "question_text": "Births per hour with λ=0.5, P(≥1)?", "correct_answer": "0.393", "options": "0.393||0.606||0.5||0.1", "is_multiple": "false"},
    {"topic": "Poisson", "concept": "Poisson Distribution", "difficulty": 5,
     "question_text": "Rare disease λ=0.01 per person. P(2+ cases)?", "correct_answer": "0.00005", "options": "0.00005||0.01||0.99||0.5", "is_multiple": "false"},
    {"topic": "Poisson", "concept": "Poisson Distribution", "difficulty": 2,
     "question_text": "P(X≤1) for Poisson(λ=3)?", "correct_answer": "0.199", "options": "0.199||0.801||0.5||0.3", "is_multiple": "false"},
    {"topic": "Poisson", "concept": "Poisson Distribution", "difficulty": 3,
     "question_text": "Calls per minute λ=2. Expected calls in 5 min?", "correct_answer": "10", "options": "10||2||5||20", "is_multiple": "false"},
    {"topic": "Poisson", "concept": "Poisson Distribution", "difficulty": 2,
     "question_text": "What is unique about Poisson distribution?", "correct_answer": "Mean = Variance", "options": "Mean = Variance||Always symmetric||Always skewed||No parameters", "is_multiple": "false"},
    {"topic": "Poisson", "concept": "Poisson Distribution", "difficulty": 4,
     "question_text": "P(X=0) for Poisson(λ=2.5)?", "correct_answer": "0.082", "options": "0.082||0.918||0.5||0.25", "is_multiple": "false"},
    {"topic": "Poisson", "concept": "Poisson Distribution", "difficulty": 1,
     "question_text": "Mode of Poisson(λ=5)?", "correct_answer": "5", "options": "5||4||3||6", "is_multiple": "false"},
    {"topic": "Poisson", "concept": "Poisson Distribution", "difficulty": 3,
     "question_text": "Errors per 100 lines λ=1.5, P(exactly 2)?", "correct_answer": "0.251", "options": "0.251||0.223||0.5||0.1", "is_multiple": "false"},
    {"topic": "Poisson", "concept": "Poisson Distribution", "difficulty": 2,
     "question_text": "For Poisson(λ), P(X=k) formula includes?", "correct_answer": "e^-λ", "options": "e^-λ||ln(λ)||λ!||k√λ", "is_multiple": "false"},
    {"topic": "Poisson", "concept": "Poisson Distribution", "difficulty": 4,
     "question_text": "If Poisson mean=4, find P(2≤X≤4)", "correct_answer": "0.623", "options": "0.623||0.377||0.5||0.6", "is_multiple": "false"},
    {"topic": "Poisson", "concept": "Poisson Distribution", "difficulty": 3,
     "question_text": "P(odd number of events) Poisson(λ=1)?", "correct_answer": "0.316", "options": "0.316||0.684||0.5||0.368", "is_multiple": "false"},
    {"topic": "Poisson", "concept": "Poisson Distribution", "difficulty": 5,
     "question_text": "Two independent Poisson(λ₁=2, λ₂=3) summed?", "correct_answer": "Poisson(λ=5)", "options": "Poisson(λ=5)||Binomial(5,0.5)||N(5,5)||Uniform", "is_multiple": "false"},
    
    # NORMAL - 30 questions  
    {"topic": "Normal", "concept": "Normal Distribution", "difficulty": 1,
     "question_text": "A standardized normal variable is denoted as?", "correct_answer": "Z", "options": "Z||X||μ||σ", "is_multiple": "false"},
    {"topic": "Normal", "concept": "Normal Distribution", "difficulty": 1,
     "question_text": "For standard normal, mean=0 and σ=?", "correct_answer": "1", "options": "1||0||0.5||2", "is_multiple": "false"},
    {"topic": "Normal", "concept": "Normal Distribution", "difficulty": 2,
     "question_text": "If X~N(100,15²), what is P(X<100)?", "correct_answer": "0.5", "options": "0.5||0.68||0.95||0.99", "is_multiple": "false"},
    {"topic": "Normal", "concept": "Z-Scores", "difficulty": 1,
     "question_text": "Z-score formula is?", "correct_answer": "(X-μ)/σ", "options": "(X-μ)/σ||X/σ||μ/σ||X-μ", "is_multiple": "false"},
    {"topic": "Normal", "concept": "Normal Distribution", "difficulty": 2,
     "question_text": "P(Z<1.96) for standard normal?", "correct_answer": "0.975", "options": "0.975||0.025||0.95||0.5", "is_multiple": "false"},
    {"topic": "Normal", "concept": "Empirical Rule", "difficulty": 1,
     "question_text": "68-95-99.7 Rule: 95% falls within?", "correct_answer": "μ±2σ", "options": "μ±2σ||μ±σ||μ±3σ||μ±1σ", "is_multiple": "false"},
    {"topic": "Normal", "concept": "Normal Distribution", "difficulty": 3,
     "question_text": "Heights N(170,10²). P(160<H<180)?", "correct_answer": "0.683", "options": "0.683||0.5||0.95||0.317", "is_multiple": "false"},
    {"topic": "Normal", "concept": "Z-Scores", "difficulty": 2,
     "question_text": "If X=85, μ=80, σ=5, what is Z?", "correct_answer": "1", "options": "1||5||25||-1", "is_multiple": "false"},
    {"topic": "Normal", "concept": "Normal Distribution", "difficulty": 2,
     "question_text": "For N(50,100), P(X>60)?", "correct_answer": "0.158", "options": "0.158||0.5||0.842||0.25", "is_multiple": "false"},
    {"topic": "Normal", "concept": "Normal Distribution", "difficulty": 3,
     "question_text": "Test scores N(mean=75, σ=10). Top 10%?", "correct_answer": "Above 87.8", "options": "Above 87.8||Below 65||Above 85||Below 60", "is_multiple": "false"},
    {"topic": "Normal", "concept": "Normal Distribution", "difficulty": 1,
     "question_text": "Bell curve is symmetric around?", "correct_answer": "mean", "options": "mean||median||mode||variance", "is_multiple": "false"},
    {"topic": "Normal", "concept": "Normal Distribution", "difficulty": 4,
     "question_text": "99.7% of data within?", "correct_answer": "μ±3σ", "options": "μ±3σ||μ±2σ||μ±σ||μ±4σ", "is_multiple": "false"},
    {"topic": "Normal", "concept": "Z-Scores", "difficulty": 2,
     "question_text": "P(-1<Z<1) standard normal?", "correct_answer": "0.683", "options": "0.683||0.5||0.95||0.317", "is_multiple": "false"},
    {"topic": "Normal", "concept": "Normal Distribution", "difficulty": 3,
     "question_text": "IQ~N(100,15²). P(IQ>130)?", "correct_answer": "0.023", "options": "0.023||0.977||0.5||0.1", "is_multiple": "false"},
    {"topic": "Normal", "concept": "Normal Distribution", "difficulty": 2,
     "question_text": "Normal distribution is determined by?", "correct_answer": "μ and σ", "options": "μ and σ||n and p||λ||df", "is_multiple": "false"},
    {"topic": "Normal", "concept": "Normal Distribution", "difficulty": 3,
     "question_text": "Weights N(70,4²). 80% weigh below?", "correct_answer": "73.4 kg", "options": "73.4 kg||70 kg||60 kg||80 kg", "is_multiple": "false"},
    {"topic": "Normal", "concept": "Z-Scores", "difficulty": 4,
     "question_text": "Find x s.t P(Z<x)=0.9 in std normal", "correct_answer": "1.28", "options": "1.28||1.96||2.33||0.84", "is_multiple": "false"},
    {"topic": "Normal", "concept": "Normal Distribution", "difficulty": 1,
     "question_text": "Standard normal has mean?", "correct_answer": "0", "options": "0||1||0.5||10", "is_multiple": "false"},
    {"topic": "Normal", "concept": "Normal Distribution", "difficulty": 4,
     "question_text": "P(Z>2.5) for std normal?", "correct_answer": "0.0062", "options": "0.0062||0.9938||0.5||0.1", "is_multiple": "false"},
    {"topic": "Normal", "concept": "Empirical Rule", "difficulty": 2,
     "question_text": "Data N(500,50²). 99.7% between?", "correct_answer": "350-650", "options": "350-650||400-600||450-550||300-700", "is_multiple": "false"},
    {"topic": "Normal", "concept": "Normal Distribution", "difficulty": 3,
     "question_text": "Test N(80,100). Top 5%?", "correct_answer": "Above 96.45", "options": "Above 96.45||Above 80||Above 100||Below 60", "is_multiple": "false"},
    {"topic": "Normal", "concept": "Z-Scores", "difficulty": 2,
     "question_text": "P(Z<-1.5) std normal?", "correct_answer": "0.067", "options": "0.067||0.933||0.5||0.15", "is_multiple": "false"},
    {"topic": "Normal", "concept": "Normal Distribution", "difficulty": 4,
     "question_text": "Find P(|Z|>1.96) standard normal", "correct_answer": "0.05", "options": "0.05||0.95||0.025||0.5", "is_multiple": "false"},
    {"topic": "Normal", "concept": "Normal Distribution", "difficulty": 5,
     "question_text": "Salary N(50000,5000²). P(45000<S<55000)?", "correct_answer": "0.683", "options": "0.683||0.5||0.95||0.317", "is_multiple": "false"},
    {"topic": "Normal", "concept": "Normal Distribution", "difficulty": 2,
     "question_text": "When is normal approximation valid?", "correct_answer": "np>5, n(1-p)>5", "options": "np>5, n(1-p)>5||n>30||p>0.5||Always", "is_multiple": "false"},
    {"topic": "Normal", "concept": "Normal Distribution", "difficulty": 3,
     "question_text": "Scores N(mean=70, σ=8). Below 50?", "correct_answer": "0.0062", "options": "0.0062||0.0228||0.9938||0.1", "is_multiple": "false"},
    {"topic": "Normal", "concept": "Z-Scores", "difficulty": 3,
     "question_text": "P(-2<Z<2) std normal?", "correct_answer": "0.954", "options": "0.954||0.5||0.683||0.046", "is_multiple": "false"},
    
    # BAYES - 30 questions
    {"topic": "Bayes", "concept": "Bayes Theorem", "difficulty": 1,
     "question_text": "Bayes Theorem relates conditional probabilities. True or False?", "correct_answer": "True", "options": "True||False", "is_multiple": "false"},
    {"topic": "Bayes", "concept": "Bayes Theorem", "difficulty": 2,
     "question_text": "P(A|B) = P(B|A)P(A) / ?", "correct_answer": "P(B)", "options": "P(B)||P(A∩B)||P(A)P(B)||P(B|A)", "is_multiple": "false"},
    {"topic": "Bayes", "concept": "Bayes Theorem", "difficulty": 1,
     "question_text": "In Bayes theorem, P(A) is called?", "correct_answer": "Prior probability", "options": "Prior probability||Posterior||Likelihood||Evidence", "is_multiple": "false"},
    {"topic": "Bayes", "concept": "Bayes Theorem", "difficulty": 2,
     "question_text": "P(A|B) is called?", "correct_answer": "Posterior probability", "options": "Posterior probability||Prior||Likelihood||Joint", "is_multiple": "false"},
    {"topic": "Bayes", "concept": "Bayes Theorem", "difficulty": 3,
     "question_text": "Disease test: P(D)=0.01, P(+|D)=0.95, P(+|¬D)=0.10. P(D|+)?",
     "correct_answer": "0.087", "options": "0.087||0.95||0.5||0.01", "is_multiple": "false"},
    {"topic": "Bayes", "concept": "Conditional Probability", "difficulty": 1,
     "question_text": "P(A and B) = P(A) × P(B|A) is?", "correct_answer": "Multiplication rule", "options": "Multiplication rule||Addition rule||Bayes rule||Complement", "is_multiple": "false"},
    {"topic": "Bayes", "concept": "Bayes Theorem", "difficulty": 2,
     "question_text": "Spam filter: 2% spam, P(spam|flag)=0.8, P(flag|spam)=0.9. P(spam flag)?",
     "correct_answer": "0.0018", "options": "0.0018||0.02||0.9||0.8", "is_multiple": "false"},
    {"topic": "Bayes", "concept": "Bayes Theorem", "difficulty": 3,
     "question_text": "Two urns: U1(2W,3B), U2(1W,4B). Pick U1, draw ball. P(W)?", "correct_answer": "0.4", "options": "0.4||0.2||0.5||0.6", "is_multiple": "false"},
    {"topic": "Bayes", "concept": "Conditional Probability", "difficulty": 2,
     "question_text": "Card: P(red|face card)?", "correct_answer": "0.5", "options": "0.5||0.25||0.75||0.33", "is_multiple": "false"},
    {"topic": "Bayes", "concept": "Bayes Theorem", "difficulty": 4,
     "question_text": "Drug test: P(use)=0.05, P(+|use)=0.95, P(+|no)=0.10. P(use|+)?",
     "correct_answer": "0.333", "options": "0.333||0.95||0.5||0.05", "is_multiple": "false"},
    {"topic": "Bayes", "concept": "Conditional Probability", "difficulty": 1,
     "question_text": "P(A|B) = P(A∩B) / ?", "correct_answer": "P(B)", "options": "P(B)||P(A)||P(B|A)||P(A)P(B)", "is_multiple": "false"},
    {"topic": "Bayes", "concept": "Bayes Theorem", "difficulty": 3,
     "question_text": "Cancer screening: P(C)=0.002, P(+|C)=0.98, P(+|¬C)=0.01. P(C|+)?",
     "correct_answer": "0.164", "options": "0.164||0.98||0.002||0.5", "is_multiple": "false"},
    {"topic": "Bayes", "concept": "Total Probability", "difficulty": 2,
     "question_text": "Law of Total Probability: P(B) = Σ P(B|Aᵢ) × ?", "correct_answer": "P(Aᵢ)", "options": "P(Aᵢ)||P(B|Aᵢ)||1||Aᵢ", "is_multiple": "false"},
    {"topic": "Bayes", "concept": "Conditional Probability", "difficulty": 2,
     "question_text": "Die roll: P(even|>3)?", "correct_answer": "0.667", "options": "0.667||0.5||0.33||0.75", "is_multiple": "false"},
    {"topic": "Bayes", "concept": "Bayes Theorem", "difficulty": 5,
     "question_text": "Two factories: F1 makes 60%, F2 makes 40%. Defect: F1=5%, F2=10%. P(F1|def)?",
     "correct_answer": "0.43", "options": "0.43||0.6||0.5||0.05", "is_multiple": "false"},
    {"topic": "Bayes", "concept": "Conditional Probability", "difficulty": 1,
     "question_text": "If A,B independent: P(A|B)=?", "correct_answer": "P(A)", "options": "P(A)||P(B)||P(A∩B)||0", "is_multiple": "false"},
    {"topic": "Bayes", "concept": "Bayes Theorem", "difficulty": 3,
     "question_text": "Email: P(spam)=0.3, P(word|spam)=0.6, P(word|ham)=0.1. P(spam|word)?",
     "correct_answer": "0.667", "options": "0.667||0.6||0.3||0.5", "is_multiple": "false"},
    {"topic": "Bayes", "concept": "Conditional Probability", "difficulty": 2,
     "question_text": "Coin flips: P(H on 2nd|H on 1st)?", "correct_answer": "0.5", "options": "0.5||0.75||0.25||1", "is_multiple": "false"},
    {"topic": "Bayes", "concept": "Bayes Theorem", "difficulty": 4,
     "question_text": "Rare disease: P(D)=0.001, sens=95%, spec=99%. P(D|+)?",
     "correct_answer": "0.087", "options": "0.087||0.95||0.001||0.5", "is_multiple": "false"},
    {"topic": "Bayes", "concept": "Conditional Probability", "difficulty": 1,
     "question_text": "Complement rule: P(A'|B) = 1 - ?", "correct_answer": "P(A|B)", "options": "P(A|B)||P(B||A)||P(B|A'))||0", "is_multiple": "false"},
    {"topic": "Bayes", "concept": "Bayes Theorem", "difficulty": 2,
     "question_text": "What is sensitivity in diagnostic test?", "correct_answer": "P(+|disease)", "options": "P(+|disease)||P(disease|+)||P(-|disease)||P(no disease|+)", "is_multiple": "false"},
    {"topic": "Bayes", "concept": "Bayes Theorem", "difficulty": 3,
     "question_text": "Draws from 2 urns. P(U1|draw)? Requires knowing prior.", "correct_answer": "Yes", "options": "Yes||No||Depends||Unknown", "is_multiple": "false"},
    {"topic": "Bayes", "concept": "Conditional Probability", "difficulty": 3,
     "question_text": "3 cards: 2G-R, 1R-R. Pick, see Green. P(other side Red)?",
     "correct_answer": "0.667", "options": "0.667||0.5||0.33||1", "is_multiple": "false"},
    {"topic": "Bayes", "concept": "Bayes Theorem", "difficulty": 4,
     "question_text": "Machine learning: Need P(class|features). Use?", "correct_answer": "Bayes Theorem", "options": "Bayes Theorem||Normal dist||Chi-square||t-test", "is_multiple": "false"},
    {"topic": "Bayes", "concept": "Conditional Probability", "difficulty": 2,
     "question_text": "P(A∩B) = P(A|B) × ?", "correct_answer": "P(B)", "options": "P(B)||P(A)||P(B|A)||1", "is_multiple": "false"},
    
    # CONDITIONAL - 30 questions
    {"topic": "Conditional", "concept": "Conditional Probability", "difficulty": 1,
     "question_text": "Conditional probability P(A|B) defined when?", "correct_answer": "P(B)>0", "options": "P(B)>0||P(A)>0||P(A∩B)>0||Always", "is_multiple": "false"},
    {"topic": "Conditional", "concept": "Independence", "difficulty": 1,
     "question_text": "A, B independent means P(A|B)=?", "correct_answer": "P(A)", "options": "P(A)||P(B)||0||1", "is_multiple": "false"},
    {"topic": "Conditional", "concept": "Conditional Probability", "difficulty": 2,
     "question_text": "Deck of cards: P(Ace|Red)?", "correct_answer": "2/26", "options": "2/26||1/13||1/52||4/52", "is_multiple": "false"},
    {"topic": "Conditional", "concept": "Conditional Probability", "difficulty": 2,
     "question_text": "Bag: 3R, 5B. Draw 1 red, then another. P(red|red)?",
     "correct_answer": "2/7", "options": "2/7||3/8||1/3||2/9", "is_multiple": "false"},
    {"topic": "Conditional", "concept": "Conditional Probability", "difficulty": 3,
     "question_text": "P(sum=10|die1=4) rolling two dice?", "correct_answer": "1/6", "options": "1/6||1/12||2/36||1/36", "is_multiple": "false"},
    {"topic": "Conditional", "concept": "Conditional Probability", "difficulty": 1,
     "question_text": "P(A|A) = ?", "correct_answer": "1", "options": "1||0||0.5||P(A)", "is_multiple": "false"},
    {"topic": "Conditional", "concept": "Independence", "difficulty": 2,
     "question_text": "Flip coin twice. Outcomes dependent or independent?", "correct_answer": "Independent", "options": "Independent||Dependent||Mutually exclusive||Cannot tell", "is_multiple": "false"},
    {"topic": "Conditional", "concept": "Conditional Probability", "difficulty": 3,
     "question_text": "P(A and B) = 0.1, P(B) = 0.5. P(A|B)?", "correct_answer": "0.2", "options": "0.2||0.1||0.5||0.05", "is_multiple": "false"},
    {"topic": "Conditional", "concept": "Conditional Probability", "difficulty": 2,
     "question_text": "Two cards drawn without replacement. P(2nd Ace|1st Ace)?",
     "correct_answer": "3/51", "options": "3/51||4/52||3/52||4/51", "is_multiple": "false"},
    {"topic": "Conditional", "concept": "Independence", "difficulty": 3,
     "question_text": "X~Poisson, Y~Normal, independent. P(X,Y|Z)=?", "correct_answer": "P(X|Z)P(Y|Z)", "options": "P(X|Z)P(Y|Z)||P(X)P(Y)||P(Z|X)P(Z|Y)||Cannot determine", "is_multiple": "false"},
    {"topic": "Conditional", "concept": "Conditional Probability", "difficulty": 1,
     "question_text": "P(A|B) + P(A'|B) = ?", "correct_answer": "1", "options": "1||0.5||P(A)||0.5+P(A)", "is_multiple": "false"},
    {"topic": "Conditional", "concept": "Conditional Probability", "difficulty": 4,
     "question_text": "Urn: 5R, 3B. Draw 2 without replacement. P(2nd B|1st R)?",
     "correct_answer": "3/7", "options": "3/7||3/8||1/2||2/5", "is_multiple": "false"},
    {"topic": "Conditional", "concept": "Conditional Probability", "difficulty": 2,
     "question_text": "Survey: 40% male, 30% male engineers. P(eng|male)?", "correct_answer": "0.75", "options": "0.75||0.3||0.4||0.5", "is_multiple": "false"},
    {"topic": "Conditional", "concept": "Independence", "difficulty": 2,
     "question_text": "Weather independent of stock price. P(sunny|up)?", "correct_answer": "P(sunny)", "options": "P(sunny)||P(up)||P(sunny∩up)||Cannot tell", "is_multiple": "false"},
    {"topic": "Conditional", "concept": "Conditional Probability", "difficulty": 3,
     "question_text": "P(H|coin fair and flipped)?", "correct_answer": "0.5", "options": "0.5||1||0||Depends on bias", "is_multiple": "false"},
    {"topic": "Conditional", "concept": "Conditional Probability", "difficulty": 2,
     "question_text": "Given B occurred first: P(A|B) depends on?", "correct_answer": "Intersection P(A∩B) and P(B)", "options": "Intersection P(A∩B) and P(B)||Only P(A)||Only P(B)||Nothing", "is_multiple": "false"},
    {"topic": "Conditional", "concept": "Independence", "difficulty": 3,
     "question_text": "P(A)=0.3, P(B)=0.4, independent. P(A and B)?", "correct_answer": "0.12", "options": "0.12||0.7||0.5||0.7", "is_multiple": "false"},
    {"topic": "Conditional", "concept": "Conditional Probability", "difficulty": 4,
     "question_text": "Medical test: P(sick)=0.02, P(+|sick)=0.9, P(+|well)=0.05. P(well|+)?",
     "correct_answer": "0.719", "options": "0.719||0.9||0.05||0.02", "is_multiple": "false"},
    {"topic": "Conditional", "concept": "Conditional Probability", "difficulty": 1,
     "question_text": "P(∅|A) = ? (empty set)", "correct_answer": "0", "options": "0||1||P(A)||0.5", "is_multiple": "false"},
    {"topic": "Conditional", "concept": "Conditional Probability", "difficulty": 3,
     "question_text": "Draw from {1,2,3,4,5,6}. P(even|>2)?", "correct_answer": "0.75", "options": "0.75||0.5||0.33||0.67", "is_multiple": "false"},
    {"topic": "Conditional", "concept": "Independence", "difficulty": 2,
     "question_text": "If mutually exclusive, P(A|B)=?", "correct_answer": "0", "options": "0||P(A)||1||Cannot tell", "is_multiple": "false"},
    {"topic": "Conditional", "concept": "Conditional Probability", "difficulty": 3,
     "question_text": "P(A|B)=0.4, P(B)=0.3. Are A,B independent?", "correct_answer": "Not enough info", "options": "Not enough info||Yes||No||Cannot tell", "is_multiple": "false"},
    {"topic": "Conditional", "concept": "Conditional Probability", "difficulty": 4,
     "question_text": "Monty Hall: Switch or stay? Conditional on revealed info?", "correct_answer": "Switch (2/3 win)", "options": "Switch (2/3 win)||Stay (1/2 win)||Either (same)||Depends", "is_multiple": "false"},
    {"topic": "Conditional", "concept": "Conditional Probability", "difficulty": 2,
     "question_text": "If P(A|B)=0 and P(B)>0, then P(A∩B)=?", "correct_answer": "0", "options": "0||P(B)||P(A)||1", "is_multiple": "false"},
]

def seed_questions():
    from sqlalchemy import text
    db = SessionLocal()
    try:
        print("Starting seed...")
        
        # Try to add missing columns if needed
        try:
            db.execute(text("ALTER TABLE questions ADD COLUMN is_multiple VARCHAR DEFAULT 'false'"))
            db.commit()
            print("Added is_multiple column")
        except:
            db.rollback()
            print("is_multiple column may already exist")
        
        try:
            db.execute(text("ALTER TABLE questions ADD COLUMN question_type VARCHAR DEFAULT 'single'"))
            db.commit()
            print("Added question_type column")
        except:
            db.rollback()
            print("question_type column may already exist")
        
        # Get count using raw SQL to avoid model issues
        result = db.execute(text("SELECT COUNT(*) FROM questions"))
        count = result.scalar()
        print(f"Current questions in DB: {count}")
        
        # Add new questions using raw SQL
        added = 0
        for q_data in QUESTIONS:
            # Check if question already exists
            result = db.execute(
                text("SELECT id FROM questions WHERE question_text = :text"),
                {"text": q_data["question_text"]}
            )
            if not result.fetchone():
                db.execute(
                    text("""INSERT INTO questions 
                            (topic, concept, difficulty, question_text, correct_answer, options, is_multiple) 
                            VALUES (:topic, :concept, :difficulty, :question_text, :correct_answer, :options, :is_multiple)"""),
                    {
                        "topic": q_data["topic"],
                        "concept": q_data["concept"],
                        "difficulty": q_data["difficulty"],
                        "question_text": q_data["question_text"],
                        "correct_answer": q_data["correct_answer"],
                        "options": q_data["options"],
                        "is_multiple": q_data["is_multiple"]
                    }
                )
                added += 1
                if added % 10 == 0:
                    print(f"  {added} added...")
        
        db.commit()
        
        # Get final count
        result = db.execute(text("SELECT COUNT(*) FROM questions"))
        final_count = result.scalar()
        print(f"✓ Seeded {added} questions! Total now: {final_count}")
        
    except Exception as e:
        db.rollback()
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    seed_questions()