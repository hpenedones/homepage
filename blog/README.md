# Blog

This is a minimalist blog setup that requires no build step or static site generator.

## Blog Organization

Posts are organized by year in subdirectories:
- `2008/` - Posts from 2008
- `2009/` - Posts from 2009
- `2010/` - Posts from 2010
- `2012/` - Posts from 2012
- `2013/` - Posts from 2013
- Root directory - New posts

This organization matches the structure of the original Blogspot blog that was imported.

## How to add a new blog post

1. **Create a new Markdown file** in this directory or in a year subdirectory (e.g., `my-new-post.md` or `2026/my-new-post.md`)
2. **Write your post** using Markdown syntax
3. **Edit `index.html`** and add your post to the `posts` array (around line 38):
   ```javascript
   const posts = [
     { file: 'my-new-post.md', title: 'My New Post Title', date: '2026-02-20' },
     { file: '2008/2008-05-31-old-post.md', title: 'Old Post Title', date: '2008-05-31' },
     { file: 'first-post.md', title: 'My First Blog Post', date: '2026-02-19' }
   ];
   ```
4. **Commit and push** - your blog post will be live!

## Importing from Blogspot

If you need to import posts from your old Blogspot blog, see [IMPORT_GUIDE.md](IMPORT_GUIDE.md) for instructions on using the `import_from_blogspot.py` script.

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
