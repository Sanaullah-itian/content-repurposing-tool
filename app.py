from flask import Flask, render_template, request
from scraper import extract_blog_content
from generator import generate_linkedin, generate_twitter, generate_email

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form.get('blog_url', '').strip()
        text = request.form.get('blog_text', '').strip()
        
        if url:
            content = extract_blog_content(url)
        elif text:
            content = text
        else:
            return render_template('index.html', error="Please enter URL or paste text.")
        
        if "Error" in content or "No content" in content:
            return render_template('index.html', error=content)
        
        linkedin = generate_linkedin(content)
        twitter = generate_twitter(content)
        email = generate_email(content)
        
        return render_template('index.html', linkedin=linkedin, twitter=twitter, email=email)
    
    return render_template('index.html')

if __name__ == '__main__':
    print("✅ App starting...")
    print("🌐 Open: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)