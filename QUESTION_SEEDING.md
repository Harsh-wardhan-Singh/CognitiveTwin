# Question Seeding Guide

## What's Fixed

✅ **Removed Question Duplication Issue**
- Removed `unique=True` constraint from `question_text` column
- Questions can now be similar without version suffixes (v34, v4, etc.)

✅ **LLM-Based Question Generation**
- Properly configured to generate 100 questions per topic
- Uses Hugging Face Meta-Llama-3 model for high-quality question generation
- Implements batch processing with retry logic for reliability

✅ **Better Error Handling**
- Gracefully skips malformed questions
- Retries failed generations up to 5 times per topic
- Provides detailed logging of generation process

## How to Run

### Step 1: Set Up HF API Key

1. Get your Hugging Face API token from: https://huggingface.co/settings/tokens
2. Create a `.env` file in the backend directory:
   ```bash
   HF_API_KEY=hf_your_token_here
   ```

### Step 2: Run the Seed Script

```bash
cd backend
python -m app.scripts.seed_questions
```

The script will:
- Check for existing questions
- Ask if you want to clear and regenerate
- Generate 100 questions per topic (6 topics × 100 = 600 questions)
- Show progress for each topic
- Report final statistics

### Step 3: Verify

Questions are now stored in PostgreSQL without duplication issues.

## Topics Covered

1. Probability Basics
2. Conditional Probability
3. Bayes Theorem
4. Random Variables
5. Distributions
6. Expectation and Variance

## Difficulty Levels

- Easy: 1
- Medium: 2 (default for seeding)
- Hard: 3

## Database Changes

- **Question Model**: `question_text` column is now `Text` without unique constraint
- **Constraint Migration**: Automatically removes old unique constraint from existing databases
- **Schema**: All other fields remain unchanged

## Troubleshooting

### "HF_API_KEY not found"
- Ensure `.env` file exists in backend directory
- Check that HF_API_KEY is set with a valid token
- Restart terminal after setting environment variables

### "No questions generated"
- Check API rate limits on Hugging Face
- Verify internet connection
- Try again after a few minutes

### "Schema validation failed"
- The LLM response doesn't match expected format
- Script will retry automatically
- If persistent, check Hugging Face API status

## Generated Questions Format

Each question includes:
- `question_text`: The actual question (< 30 words)
- `options`: 4-6 multiple choice options with IDs (A, B, C, D, E, F)
- `correct_answer`: Pipe-separated list of correct option IDs (e.g., "A|B")
- `difficulty`: 1 (easy), 2 (medium), or 3 (hard)
- `question_type`: "single" or "multiple"
- `is_multiple`: "true" or "false"

## Database Schema

```sql
CREATE TABLE questions (
  id SERIAL PRIMARY KEY,
  topic VARCHAR,
  concept VARCHAR,
  difficulty INTEGER,
  question_text TEXT,  -- No unique constraint
  correct_answer VARCHAR,
  options TEXT,
  question_type VARCHAR DEFAULT 'single',
  is_multiple VARCHAR DEFAULT 'false'
);
```

---

**Note**: The seeding process may take 10-20 minutes depending on API response times.
