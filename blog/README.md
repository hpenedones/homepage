# Blog

This is a minimalist blog setup that requires no build step or static site generator.

## How to add a new blog post

1. **Create a new Markdown file** in this directory (e.g., `my-new-post.md`)
2. **Write your post** using Markdown syntax
3. **Edit `index.html`** and add your post to the `posts` array (around line 31):
   ```javascript
   const posts = [
     { file: 'my-new-post.md', title: 'My New Post Title', date: '2026-02-20' },
     { file: 'first-post.md', title: 'My First Blog Post', date: '2026-02-19' }
   ];
   ```
4. **Commit and push** - your blog post will be live!

## How it works

- Blog posts are written as Markdown files (`.md`)
- The `index.html` page lists all blog posts
- The `post.html` page renders individual posts using the [marked.js](https://marked.js.org/) library
- No build step required - it all works client-side with GitHub Pages

## Markdown features

You can use standard Markdown syntax including:
- Headers (`#`, `##`, `###`)
- Lists (ordered and unordered)
- Links `[text](url)`
- Code blocks with syntax highlighting
- Bold and italic text
- Blockquotes
- And more!
