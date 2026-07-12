def generate_linkedin(text):
    print("🔨 Generating LinkedIn (Mock)...")
    # Text ko LinkedIn style mein convert karo
    lines = text.split('. ')
    post = "🚀 " + lines[0] + ".\n\n"
    post += "💡 " + (lines[1] if len(lines) > 1 else "This is a game-changer for professionals.") + "\n\n"
    post += "✅ " + (lines[2] if len(lines) > 2 else "The benefits are undeniable.") + "\n\n"
    post += "What are your thoughts on this? Let's discuss in the comments! 👇\n\n"
    post += "#ProfessionalGrowth #Innovation #Leadership"
    return post

def generate_twitter(text):
    print("🔨 Generating Twitter (Mock)...")
    # Chhoti chhoti tweets mein tod do
    words = text.split()
    part_size = len(words) // 5
    tweets = []
    for i in range(5):
        start = i * part_size
        end = start + part_size
        tweet_text = ' '.join(words[start:end])
        if len(tweet_text) > 270:
            tweet_text = tweet_text[:270] + "..."
        tweets.append(f"{i+1}/5: {tweet_text}")
    
    return "\n\n".join(tweets)

def generate_email(text):
    print("🔨 Generating Email (Mock)...")
    # Email format mein daalo
    subject = "📧 Newsletter: " + text.split('.')[0][:50]
    body = f"Subject: {subject}\n\n"
    body += "Dear Reader,\n\n"
    body += text + "\n\n"
    body += "We hope you found this insightful. Stay tuned for more updates!\n\n"
    body += "Best regards,\nThe Content Team"
    return body