# How to Fix the HF API Key Issue

## The Problem
The Hugging Face API token in your `.env` file is returning a `401 Unauthorized` error, which means:
- The token is invalid or expired
- The token doesn't have inference permissions
- The token was revoked

## Step-by-Step Fix

### Step 1: Generate a New Token

1. Go to https://huggingface.co/settings/tokens
2. Click **"New token"** button
3. Set the following:
   - **Name**: `cognitive-twin-inference` (or any name you prefer)
   - **Type**: Select "**Fine-grained token**"
   - **Permissions**: Make sure these are checked:
     - ✅ `repo.content.read` (read repository content)
     - ✅ `inference-api` (use inference API)
   - **Repositories access**: Select "All public and private repos" or at least allow the Llama models

### Step 2: Copy the Generated Token

1. The token will appear (looks like `hf_xxxxxxxxxxxxxxxxxxxxx`)
2. Copy it to your clipboard

### Step 3: Update Your .env File

1. Open `backend/.env`
2. Replace the old HF_API_KEY with the new one:
   ```
   HF_API_KEY=hf_your_new_token_here
   ```
3. Save the file

### Step 4: Test the New Token

```bash
cd backend
python test_llm_diagnostic.py
```

You should see:
```
✓ ALL TESTS PASSED - Ready to seed database!
```

### Step 5: Run the Seeding Script

```bash
cd backend
python -m app.scripts.seed_questions
```

## Troubleshooting

If you still get 401 errors:
1. Double-check you copied the token correctly
2. Verify the token has "inference-api" permission enabled
3. Try creating a new token with the steps above
4. Check if your HF account has API access enabled (some regions/plans may have restrictions)

## Alternative Approach (if HF continues to fail)

If the Hugging Face API continues to have issues, you could:
1. Use a different LLM provider (OpenAI, Anthropic, Together AI, etc.)
2. Use a local LLM (though this would require more setup)
3. Use pre-generated questions for now

For now, focus on getting the HF token working by following the steps above.
