#!/usr/bin/env python3
"""
Script to import blog posts from Blogspot (aboutintelligence.blogspot.com) to markdown files.

This script:
1. Fetches all posts from the Blogspot feed
2. Converts HTML content to Markdown
3. Organizes posts by year in separate directories (2008/, 2009/, etc.)
4. Generates a posts array for blog/index.html

Usage:
    python3 import_from_blogspot.py

Requirements:
    - Python 3.6+
    - Internet connection
    - No external dependencies (uses only standard library)
"""

import os
import re
import json
import urllib.request
import urllib.error
from datetime import datetime
from html.parser import HTMLParser

class HTMLToMarkdown(HTMLParser):
    """Simple HTML to Markdown converter."""

    def __init__(self):
        super().__init__()
        self.markdown = []
        self.current_tag = []
        self.href = None
        self.in_pre = False
        self.in_code = False
        self.list_level = 0

    def handle_starttag(self, tag, attrs):
        self.current_tag.append(tag)
        attrs_dict = dict(attrs)

        if tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            level = int(tag[1])
            self.markdown.append('\n' + '#' * level + ' ')
        elif tag == 'p':
            self.markdown.append('\n\n')
        elif tag == 'br':
            self.markdown.append('  \n')
        elif tag == 'a':
            self.href = attrs_dict.get('href', '')
            self.markdown.append('[')
        elif tag == 'img':
            src = attrs_dict.get('src', '')
            alt = attrs_dict.get('alt', '')
            self.markdown.append(f'\n\n![{alt}]({src})\n\n')
        elif tag == 'strong' or tag == 'b':
            self.markdown.append('**')
        elif tag == 'em' or tag == 'i':
            self.markdown.append('*')
        elif tag == 'code':
            self.markdown.append('`')
            self.in_code = True
        elif tag == 'pre':
            self.markdown.append('\n\n```\n')
            self.in_pre = True
        elif tag in ['ul', 'ol']:
            self.markdown.append('\n')
            self.list_level += 1
        elif tag == 'li':
            self.markdown.append('  ' * (self.list_level - 1) + '- ')
        elif tag == 'blockquote':
            self.markdown.append('\n> ')
        elif tag == 'hr':
            self.markdown.append('\n\n---\n\n')

    def handle_endtag(self, tag):
        if self.current_tag and self.current_tag[-1] == tag:
            self.current_tag.pop()

        if tag == 'a' and self.href:
            self.markdown.append(f']({self.href})')
            self.href = None
        elif tag in ['strong', 'b']:
            self.markdown.append('**')
        elif tag in ['em', 'i']:
            self.markdown.append('*')
        elif tag == 'code':
            self.markdown.append('`')
            self.in_code = False
        elif tag == 'pre':
            self.markdown.append('\n```\n\n')
            self.in_pre = False
        elif tag in ['ul', 'ol']:
            self.markdown.append('\n')
            self.list_level -= 1
        elif tag == 'li':
            self.markdown.append('\n')
        elif tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            self.markdown.append('\n')

    def handle_data(self, data):
        # Clean up whitespace, but preserve in code blocks
        if self.in_pre or self.in_code:
            self.markdown.append(data)
        else:
            # Replace multiple spaces with single space
            cleaned = re.sub(r'\s+', ' ', data)
            if cleaned and cleaned != ' ':
                self.markdown.append(cleaned)

    def get_markdown(self):
        result = ''.join(self.markdown)
        # Clean up multiple newlines
        result = re.sub(r'\n{3,}', '\n\n', result)
        return result.strip()

def fetch_blogspot_feed(blog_url, start_index=1, max_results=500):
    """Fetch blog posts from Blogspot JSON feed."""
    feed_url = f"{blog_url}/feeds/posts/default?alt=json&start-index={start_index}&max-results={max_results}"
    print(f"Fetching: {feed_url}")

    try:
        with urllib.request.urlopen(feed_url, timeout=30) as response:
            data = json.loads(response.read().decode('utf-8'))
            return data
    except urllib.error.URLError as e:
        print(f"Error fetching feed: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

def extract_posts(feed_data):
    """Extract relevant post information from Blogspot feed."""
    if not feed_data or 'feed' not in feed_data:
        return []

    posts = []
    entries = feed_data['feed'].get('entry', [])

    for entry in entries:
        # Extract title
        title = entry.get('title', {}).get('$t', 'Untitled')

        # Extract content
        content = entry.get('content', {}).get('$t', '')

        # Extract published date
        published = entry.get('published', {}).get('$t', '')
        try:
            date_obj = datetime.fromisoformat(published.replace('Z', '+00:00'))
        except:
            print(f"Warning: Could not parse date for post: {title}")
            continue

        # Extract link
        links = entry.get('link', [])
        post_url = ''
        for link in links:
            if link.get('rel') == 'alternate':
                post_url = link.get('href', '')
                break

        posts.append({
            'title': title,
            'content': content,
            'date': date_obj,
            'url': post_url
        })

    return posts

def html_to_markdown(html_content):
    """Convert HTML content to Markdown."""
    parser = HTMLToMarkdown()
    parser.feed(html_content)
    return parser.get_markdown()

def sanitize_filename(title):
    """Convert title to a safe filename."""
    # Remove special characters and replace spaces with hyphens
    filename = re.sub(r'[^\w\s-]', '', title.lower())
    filename = re.sub(r'[-\s]+', '-', filename)
    filename = filename.strip('-')
    return filename[:100]  # Limit length

def save_posts_to_markdown(posts, output_dir):
    """Save blog posts as markdown files organized by year."""
    for post in posts:
        year = post['date'].year
        year_dir = os.path.join(output_dir, str(year))
        os.makedirs(year_dir, exist_ok=True)

        # Create filename
        date_str = post['date'].strftime('%Y-%m-%d')
        title_slug = sanitize_filename(post['title'])
        filename = f"{date_str}-{title_slug}.md"
        filepath = os.path.join(year_dir, filename)

        # Convert content to markdown
        markdown_content = html_to_markdown(post['content'])

        # Create markdown file with frontmatter
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"# {post['title']}\n\n")
            f.write(f"**Date:** {post['date'].strftime('%B %d, %Y')}\n\n")
            f.write(f"**Original URL:** {post['url']}\n\n")
            f.write("---\n\n")
            f.write(markdown_content)

        print(f"Saved: {filepath}")

def generate_posts_list(posts):
    """Generate JavaScript array for index.html."""
    posts_sorted = sorted(posts, key=lambda x: x['date'], reverse=True)  # Newest first

    js_posts = []
    for post in posts_sorted:
        year = post['date'].year
        date_str = post['date'].strftime('%Y-%m-%d')
        title_slug = sanitize_filename(post['title'])
        filename = f"{year}/{date_str}-{title_slug}.md"

        # Escape single quotes in title
        title_escaped = post['title'].replace("'", "\\'")

        js_posts.append(f"    {{ file: '{filename}', title: '{title_escaped}', date: '{date_str}' }}")

    return js_posts

def main():
    blog_url = "https://aboutintelligence.blogspot.com"
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = script_dir  # Save in blog/ directory

    print("=" * 70)
    print("Blogspot to Markdown Importer")
    print("=" * 70)
    print(f"\nFetching blog posts from: {blog_url}")
    print("This may take a few moments...\n")

    feed_data = fetch_blogspot_feed(blog_url)

    if not feed_data:
        print("\n❌ Failed to fetch blog posts.")
        print("Please check your internet connection and try again.")
        return

    print("✓ Successfully fetched feed data")
    print("\nExtracting post information...")
    posts = extract_posts(feed_data)

    print(f"✓ Found {len(posts)} posts")

    if not posts:
        print("No posts found. Exiting.")
        return

    # Sort posts by date (oldest first for display)
    posts.sort(key=lambda x: x['date'])

    # Display date range and year breakdown
    year_counts = {}
    for post in posts:
        year = post['date'].year
        year_counts[year] = year_counts.get(year, 0) + 1

    print(f"\nDate range: {posts[0]['date'].year} to {posts[-1]['date'].year}")
    print("\nPosts by year:")
    for year in sorted(year_counts.keys()):
        print(f"  {year}: {year_counts[year]} posts")

    print("\n" + "=" * 70)
    print("Saving posts to markdown files...")
    print("=" * 70 + "\n")

    save_posts_to_markdown(posts, output_dir)

    print("\n" + "=" * 70)
    print("Generating posts array for index.html...")
    print("=" * 70 + "\n")

    js_posts = generate_posts_list(posts)

    # Save to a file for easy copying
    output_file = os.path.join(script_dir, "posts_array.js")
    with open(output_file, 'w') as f:
        f.write("// Copy this array and replace the 'posts' array in blog/index.html\n")
        f.write("// (around line 38)\n\n")
        f.write("const posts = [\n")
        f.write(",\n".join(js_posts))
        f.write("\n];\n")

    print(f"✓ Posts array saved to: {output_file}")
    print("\n" + "=" * 70)
    print("✅ Import complete!")
    print("=" * 70)
    print("\nNext steps:")
    print("1. Open blog/posts_array.js")
    print("2. Copy the posts array")
    print("3. Replace the posts array in blog/index.html (around line 38)")
    print("4. Commit and push your changes")
    print("\nAll blog posts have been imported and organized by year!")

if __name__ == "__main__":
    main()
